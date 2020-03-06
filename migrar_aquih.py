import sys
import psycopg2

def update(cur, tabla, columnas):
    columnas_select = ", ".join(columnas)
    columnas_update = ", ".join([x+" = %s" for x in columnas[: -1]])

    cur.execute("select {} from {}".format(columnas_select, tabla))
    for l in cur:
        print cur.mogrify("update {} set {} where id = %s;".format(tabla, columnas_update), l)

def insert(cur, tabla, columnas):
    columnas_select = ", ".join(columnas)
    columnas_insert = ", ".join(["%s" for x in columnas])

    cur.execute("select {} from {}".format(columnas_select, tabla))
    for l in cur:
        print cur.mogrify("insert into {} ({}) values ({});".format(tabla, columnas_select, columnas_insert), l)

    print cur.mogrify("select setval('{}_seq', (select max(id) from {})+1);".format(tabla, tabla))

conn = psycopg2.connect("dbname={} user={}".format(sys.argv[1], sys.argv[2]))
cur = conn.cursor()

# albaran_analitico
if 'albaran_analitico' in sys.argv:
    update(cur, "stock_picking", ["cuenta_analitica_id", "id"])
    update(cur, "stock_inventory", ["cuenta_analitica_id", "id"])

# bolson
if 'bolson' in sys.argv:
    print("update account_invoice set bolson_id = null from bolson_bolson where bolson_id = null;")
    print("update account_payment set bolson_id = null from bolson_bolson where bolson_id = null;")
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
    insert(cur, "pos_gt_extra_product_template_rel", ["product_template_id", "pos_gt_extra_id"])
    update(cur, "res_users", ["default_pos_id", "id"])

# pos_sat
if 'pos_sat' in sys.argv:
    print("delete from pos_gt_extra_product_template_rel;")

    insert(cur, "pos_sat_resolucion", ["id", "name", "fecha", "serie", "direccion", "inicial", "final", "primera", "valido", "tipo_doc", "fecha_ingreso", "fecha_vencimiento"])
    update(cur, "account_journal", ["requiere_resolucion", "ultimo_numero_factura", "id"])
    update(cur, "ir_sequence", ["resolucion_id", "id"])
    update(cur, "pos_order", ["numero_factura_impreso", "id"])

# guateburger
if 'guateburger' in sys.argv:
    print("delete from guateburger_pedido_tienda_linea;")
    print("delete from guateburger_pedido_tienda;")
    print("delete from pos_config_product_category_rel;")

    insert(cur, "guateburger_pedido_tienda", ["id", "name", "fecha", "default_pos_id", "state"])
    # cur.execute("select id, name, fecha, default_pos_id, state from guateburger_pedido_tienda;")
    # for l in cur:
    #     print cur.mogrify("insert into guateburger_pedido_tienda (id, name, fecha, default_pos_id, state) values (%s, %s, %s, %s, %s);", l)

    insert(cur, "guateburger_pedido_tienda_linea", ["id", "pedido_tienda_id", "product_id", "uom_po_id", "cantidad"])
    # cur.execute("select id, pedido_tienda_id, product_id, uom_po_id, cantidad from guateburger_pedido_tienda_linea;")
    # for l in cur:
    #     print cur.mogrify("insert into guateburger_pedido_tienda_linea (id, pedido_tienda_id, product_id, uom_po_id, cantidad) values (%s, %s, %s, %s, %s);", l)

    update(cur, "pos_config", ["tipo_impresora", "id"])
    # cur.execute("select tipo_impresora, id from pos_config;")
    # for l in cur:
    #     print cur.mogrify("update pos_config set tipo_impresora = %s where id = %s;", l)

    insert(cur, "pos_config_product_category_rel", ["pos_config_id", "product_category_id"])
    # cur.execute("select pos_config_id, product_category_id from pos_config_product_category_rel;")
    # for l in cur:
    #     print cur.mogrify("insert into pos_config_product_category_rel (pos_config_id, product_category_id) values (%s, %s);", l)

    update(cur, "purchase_order", ["fecha_recepcion_factura", "fecha_pago", "numero_factura", "id"])
    # cur.execute("select fecha_recepcion_factura, fecha_pago, numero_factura, id from purchase_order;")
    # for l in cur:
    #     print cur.mogrify("update purchase_order set fecha_recepcion_factura = %s, fecha_pago = %s, numero_factura = %s where id = %s;", l)

    update(cur, "account_invoice", ["fecha_pago", "id"])
    # cur.execute("select fecha_pago, id from account_invoice;")
    # for l in cur:
    #     print cur.mogrify("update account_invoice set fecha_pago = %s where id = %s;", l)

    update(cur, "res_partner", ["fecha_pago", "id"])
    # cur.execute("select fecha_pago, id from res_partner;")
    # for l in cur:
    #     print cur.mogrify("update res_partner set fecha_pago = %s where id = %s;", l)

cur.close()
conn.close()