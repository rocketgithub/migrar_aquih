import sys
import psycopg2

def update(cur, tabla, columnas):
    columnas_select = ", ".join(columnas)
    columnas_update = ", ".join([x+" = %s" for x in columnas[: -1]])

    cur.execute("select {} from {}".format(columnas_select, tabla))
    for l in cur:
        print cur.mogrify("update {} set {} where id = %s;".format(tabla, columnas_update), l)

def insert(cur, tabla, columnas, set_sequence=True):
    columnas_select = ", ".join(columnas)
    columnas_insert = ", ".join(["%s" for x in columnas])

    cur.execute("select {} from {}".format(columnas_select, tabla))
    for l in cur:
        print cur.mogrify("insert into {} ({}) values ({});".format(tabla, columnas_select, columnas_insert), l)

    if set_sequence is True:
        print cur.mogrify("select setval('{}_id_seq', (select max(id) from {})+1);".format(tabla, tabla))

conn = psycopg2.connect("dbname={} user={}".format(sys.argv[1], sys.argv[2]))
cur = conn.cursor()

# albaran_analitico
if 'albaran_analitico' in sys.argv:
    update(cur, "stock_picking", ["cuenta_analitica_id", "id"])
    update(cur, "stock_inventory", ["cuenta_analitica_id", "id"])

# bolson
if 'bolson' in sys.argv:
    print("update account_invoice set bolson_id = null from bolson_bolson where bolson_id is not null;")
    print("update account_payment set bolson_id = null from bolson_bolson where bolson_id is not null;")
    print("delete from bolson_bolson;")

    insert(cur, "bolson_bolson", ["id", "asiento", "create_uid", "name", "diario", "company_id", "create_date", "write_date", "cuenta_desajuste", "write_uid", "fecha", "usuario_id"])
    update(cur, "account_invoice", ["bolson_id", "id"])
    update(cur, "account_payment", ["bolson_id", "id"])

# conciliacion_bancaria
if 'conciliacion_bancaria' in sys.argv:
    print("delete from conciliacion_bancaria_fecha;")

    insert(cur, "conciliacion_bancaria_fecha", ["id", "create_uid", "create_date", "fecha", "write_uid", "write_date", "move_id"])

# gface_infile
if 'gface_infile' in sys.argv:
    update(cur, "account_invoice", ["firma_gface", "pdf_gface", "id"])
    update(cur, "account_journal", ["usuario_gface", "clave_gface", "nombre_establecimiento_gface", "tipo_documento_gface", "serie_documento_gface", "serie_gface", "numero_resolucion_gface", "fecha_resolucion_gface", "rango_inicial_gface", "rango_final_gface", "numero_establecimiento_gface", "dispositivo_gface", "id"])

# l10n_gt_extra
if 'l10n_gt_extra' in sys.argv:
    update(cur, "account_invoice", ["tipo_gasto", "numero_viejo", "id"])
    update(cur, "account_payment", ["numero_viejo", "nombre_impreso", "id"])
    update(cur, "account_journal", ["direccion", "id"])
    update(cur, "res_partner", ["pequenio_contribuyente", "id"])

# pos_gt
if 'pos_gt' in sys.argv:
    print("delete from pos_gt_bom_extra_line;")
    print("delete from pos_gt_extra_line;")
    print("delete from pos_gt_extra;")
    print("delete from pos_gt_extra_product_template_rel;")

    insert(cur, "pos_gt_bom_extra_line", ["id", "name", "product_id", "product_qty", "product_uom_id", "bom_id"])
    update(cur, "pos_config", ["allow_discount", "allow_price_change", "ask_tag_number", "takeout_option", "default_client_id", "analytic_account_id", "id"])
    insert(cur, "pos_gt_extra", ["id", "name", "company_id", "type"])
    insert(cur, "pos_gt_extra_line", ["id", "name", "extra_id", "product_id", "qty", "price_extra", "company_currency_id"])
    insert(cur, "pos_gt_extra_product_template_rel", ["product_template_id", "pos_gt_extra_id"], set_sequence=False)
    update(cur, "res_users", ["default_pos_id", "id"])

# pos_sat
if 'pos_sat' in sys.argv:
    insert(cur, "pos_sat_resolucion", ["id", "name", "fecha", "serie", "direccion", "inicial", "final", "primera", "valido", "tipo_doc", "fecha_ingreso", "fecha_vencimiento"])
    update(cur, "account_journal", ["requiere_resolucion", "ultimo_numero_factura", "id"])
    update(cur, "ir_sequence", ["resolucion_id", "id"])
    update(cur, "pos_order", ["numero_factura_impreso", "id"])

# fel_infile
if 'fel_infile' in sys.argv:
    update(cur, "account_invoice", ["serie_fel", "numero_fel", "pdf_fel", "factura_original_id", "id"])
    update(cur, "account_journal", ["usuario_fel", "clave_fel", "token_firma_fel", "codigo_establecimiento_fel", "tipo_documento_fel", "id"])
    update(cur, "res_company", ["frases_fel", "adenda_fel", "id"])

# importaciones
if 'importaciones' in sys.argv:
    print("delete from account_tax_importaciones_poliza_linea_rel;")
    print("delete from account_invoice_importaciones_poliza_linea_rel;")
    print("delete from importaciones_gasto_asociado_importaciones_poliza_linea_rel;")
    print("delete from importaciones_gasto_asociado;")
    print("delete from importaciones_documento_asociado;")
    print("delete from importaciones_poliza_linea;")
    print("delete from importaciones_poliza;")
    print("delete from importaciones_tipo_gasto;")

    insert(cur, "importaciones_tipo_gasto", ["id", "name"])
    insert(cur, "importaciones_poliza", ["id", "name", "fecha", "company_id", "poliza_aduana", "tipo_importacion", "guia", "transportista_id", "comentario", "moneda_base_id", "moneda_compra_id", "tasa", "arancel_total", "state"])
    insert(cur, "importaciones_poliza_linea", ["id", "name", "poliza_id", "producto_id", "pedido", "cantidad", "impuestos_importacion_manual", "impuestos", "precio", "costo_proyectado", "costo", "porcentage_gasto", "porcentage_gasto_importacion", "total_gastos", "total_gastos_importacion", "costo_asignado"])
    insert(cur, "importaciones_documento_asociado", ["id", "name", "poliza_id", "factura_id", "tipo_gasto_id"])
    insert(cur, "importaciones_gasto_asociado", ["id", "name", "poliza_id", "valor", "tipo_gasto_id"])
    insert(cur, "importaciones_gasto_asociado_importaciones_poliza_linea_rel", ["importaciones_poliza_linea_id", "importaciones_gasto_asociado_id"], set_sequence=False)
    insert(cur, "account_invoice_importaciones_poliza_linea_rel", ["importaciones_poliza_linea_id", "account_invoice_id"], set_sequence=False)
    insert(cur, "account_tax_importaciones_poliza_linea_rel", ["importaciones_poliza_linea_id", "account_tax_id"], set_sequence=False)
    update(cur, "purchase_order", ["poliza_id", "gasto_general_poliza", "id"])

# pos_gface
if 'pos_gface' in sys.argv:
    pass

# guateburger
if 'guateburger' in sys.argv:
    print("delete from guateburger_pedido_tienda_linea;")
    print("delete from guateburger_pedido_tienda;")
    print("delete from pos_config_product_category_rel;")

    insert(cur, "guateburger_pedido_tienda", ["id", "name", "fecha", "default_pos_id", "state"])
    insert(cur, "guateburger_pedido_tienda_linea", ["id", "pedido_tienda_id", "product_id", "uom_po_id", "cantidad"])
    update(cur, "pos_config", ["tipo_impresora", "id"])
    insert(cur, "pos_config_product_category_rel", ["pos_config_id", "product_category_id"], set_sequence=False)
    update(cur, "purchase_order", ["fecha_recepcion_factura", "fecha_pago", "numero_factura", "id"])
    update(cur, "account_invoice", ["fecha_pago", "id"])
    update(cur, "res_partner", ["correo_pagos", "id"])

# grupo2g
if 'grupo2g' in sys.argv:
    print("delete from grupo2g_equivalente_linea;")
    print("delete from grupo2g_linea;")
    print("delete from grupo2g_clasificacion;")
    print("delete from grupo2g_tipo;")
    print("delete from grupo2g_marca;")

    insert(cur, "grupo2g_marca", ["id", "name"])
    insert(cur, "grupo2g_tipo", ["id", "nombre", "secuencia"])
    insert(cur, "grupo2g_clasificacion", ["id", "nombre", "secuencia"])
    insert(cur, "grupo2g_linea", ["id", "producto_id", "ubicacion_id", "localidad"])
    insert(cur, "grupo2g_equivalente_linea", ["id", "producto_id", "marca", "numero", "actual"])
    update(cur, "hr_employee", ["descuento_minimo", "descuento_maximo", "comision_minima", "comision_maxima", "id"])
    update(cur, "pos_config", ["search_product_option", "id"])
    update(cur, "product_template", ["codigo_viejo", "marca_id", "marca_id", "ubicacion_linea", "tipo", "clasificacion", "secuencia", "venta_tipica", "id"])
    update(cur, "stock_location", ["picking_type_id", "id"])

cur.close()
conn.close()