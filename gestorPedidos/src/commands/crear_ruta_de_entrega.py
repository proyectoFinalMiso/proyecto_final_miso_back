import math

import requests
from src.commands.base_command import BaseCommand
from src.constants.urls import STORE_URL
from src.models.model import PackingList, Pedido, RutaDeEntrega, db


class CrearRutaDeEntrega(BaseCommand):

    def __init__(self, cuerpo_solicitud: dict):
        self.body = cuerpo_solicitud

    def verificar_campos_requeridos(self) -> bool:
        campos_requeridos = ["pedido_id"]

        if not all(campo in self.body for campo in campos_requeridos):
            return False

        if not all(self.body.get(campo) for campo in campos_requeridos):
            return False

        return True

    def obtener_inventario(self):

        url_obtener_producto = STORE_URL + "/inventario/listar_inventarios"

        headers = {
            "Content-Type": "application/json",
        }

        try:

            respuesta = requests.get(
                url_obtener_producto, json={}, headers=headers)

            if respuesta.status_code not in [200, 201]:

                raise Exception(f"Error al obtener inventario: "
                                f"Status {respuesta.status_code} - {respuesta.text}")

            return respuesta.json()["body"]

        except requests.RequestException as e:

            raise Exception(
                f"Error de conexión al hacer POST a {url_obtener_producto}: {str(e)}")

    def haversine(self, coord1, coord2):

        lat1, lon1, *_ = coord1
        lat2, lon2, *_ = coord2

        lat1, lon1 = math.radians(lat1), math.radians(lon1)
        lat2, lon2 = math.radians(lat2), math.radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * \
            math.cos(lat2) * math.sin(dlon / 2) ** 2

        c = 2 * math.asin(math.sqrt(a))

        return 6371 * c

    def calcular_distancias(self, ubicaciones):

        cantidad = len(ubicaciones)

        distancias = [[0.0 for _ in range(cantidad)]
                      for _ in range(cantidad)]

        for i in range(cantidad):

            for j in range(cantidad):

                if i != j:

                    distancias[i][j] = self.haversine(

                        ubicaciones[i], ubicaciones[j])

        return distancias

    def optimizar_ruta_algoritmo_voraz(self, distancias):

        cantidad = len(distancias)

        ruta = [0]

        restantes = list(range(1, cantidad))

        while restantes:

            ultimo = ruta[-1]

            siguiente = min(restantes, key=lambda x: distancias[ultimo][x])

            ruta.append(siguiente)

            restantes.remove(siguiente)

        return ruta

    def encontrar_ruta_optima(self, informacion_de_entrega, packing_list):

        ruta = []

        for producto_a_enviar in packing_list:

            almacenes_con_stock = [

                w for w in informacion_de_entrega if int(w["sku"]) == int(producto_a_enviar["sku"])]

            almacenes_ordenados = sorted(
                almacenes_con_stock, key=lambda a: int(a["cantidadDisponible"])
            )

            cantidad_requerida = int(producto_a_enviar["cantidadRequerida"])

            productos_recolectados = 0

            for almacen in almacenes_ordenados:

                if productos_recolectados >= cantidad_requerida:
                    break

                productos_disponibles = int(almacen["cantidadDisponible"])

                productos_necesarios = cantidad_requerida - productos_recolectados

                if productos_disponibles >= productos_necesarios:

                    productos_recolectados += productos_necesarios

                else:

                    productos_recolectados += productos_disponibles

                ruta.append(almacen)

            if productos_recolectados < cantidad_requerida:

                raise Exception(
                    f"No hay stock suficiente para el producto: {producto_a_enviar}"
                )

        coordenadas = [[c["latitude"], c["longitude"], c["nombre"]]
                       for c in ruta]

        distancias = self.calcular_distancias(coordenadas)

        ruta_optimizada = self.optimizar_ruta_algoritmo_voraz(distancias)

        ruta_final = []

        for i in ruta_optimizada:
            ruta_final.append(coordenadas[i])

        return ruta_final

    def obtener_bodega(self, id):

        url_obtener_bodega = STORE_URL + "/bodega/buscador_bodega"

        payload = {"clave": id}

        headers = {
            "Content-Type": "application/json",
        }

        try:

            respuesta = requests.get(
                url_obtener_bodega, json=payload, headers=headers)

            if respuesta.status_code not in [200, 201]:

                raise Exception(f"Error al obtener inventario: "
                                f"Status {respuesta.status_code} - {respuesta.text}")

            return respuesta.json()
        except requests.RequestException as e:

            raise Exception(
                f"Error de conexión al hacer POST a {url_obtener_bodega}: {str(e)}")

    def execute(self):

        pedido_id = self.body["pedido_id"]

        if not self.verificar_campos_requeridos():

            return {
                "response": {
                    "msg": "Campos requeridos no cumplidos"
                },
                "status_code": 400
            }

        pedido_obtenido = Pedido.query.filter_by(id=pedido_id).first()

        packing_list_id = pedido_obtenido.packingList

        packing_list_obtenido = PackingList.query.filter_by(
            listID=packing_list_id).all()

        productos_requeridos = [
            {"sku": p.producto, "cantidadRequerida": p.cantidad} for p in packing_list_obtenido]

        skus = [p.producto for p in packing_list_obtenido]

        inventario = self.obtener_inventario()

        inventario_por_sku = {str(item['sku']): item for item in inventario}

        for sku in skus:

            if sku not in inventario_por_sku:

                raise ValueError(
                    f"No hay inventario para el SKU {sku}. Proceso terminado.")

        inventario_filtrado = [inventario_por_sku[sku] for sku in skus]

        informacion_de_entrega = []

        for i, b in enumerate(inventario_filtrado):

            bodega_id = b["bodega"]

            bodega = self.obtener_bodega(bodega_id)["bodegas"][0]

            informacion_de_entrega.append(
                {**bodega, "cantidadDisponible": inventario_filtrado[i]["cantidadDisponible"], "sku": inventario_filtrado[i]["sku"]})

        self.encontrar_ruta_optima(
            informacion_de_entrega, productos_requeridos)

        ruta_sugerida = self.encontrar_ruta_optima(
            informacion_de_entrega, productos_requeridos)

        nueva_ruta_de_entrega = RutaDeEntrega(
            pedidoID=pedido_id,
            ruta=str(ruta_sugerida)
        )

        db.session.add(nueva_ruta_de_entrega)

        try:

            db.session.commit()

            return {
                "response": {
                    "msg": self.encontrar_ruta_optima(informacion_de_entrega, productos_requeridos)
                },
                "status_code": 201
            }

        except Exception as e:

            print(e)

            db.session.rollback()

            return {
                "response": {
                    "msg": f"Error al crear ruta de entrega para el pedido {pedido_id}"
                },
                "status_code": 500
            }
