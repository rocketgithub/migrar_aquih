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

conn = psycopg2.connect("dbname=grupor2c user=odoo")
cur = conn.cursor()

# albaran_analitico
if 0:
    update(cur, "stock_picking", ["cuenta_analitica_id", "id"])
    # cur.execute("select cuenta_analitica_id, id from stock_picking where cuenta_analitica_id is not null;")
    # for l in cur:
    #     print cur.mogrify("update stock_picking set cuenta_analitica_id = %s where id = %s;", l)

    update(cur, "stock_inventory", ["cuenta_analitica_id", "id"])
    # cur.execute("select cuenta_analitica_id, id from stock_inventory where cuenta_analitica_id is not null;")
    # for l in cur:
    #     print cur.mogrify("update stock_inventory set cuenta_analitica_id = %s where id = %s;", l)

# bolson
if 0:
    print("update account_invoice set bolson_id = null from bolson_bolson where bolson_id = null;")
    print("update account_payment set bolson_id = null from bolson_bolson where bolson_id = null;")
    print("delete from bolson_bolson;")

    insert(cur, "bolson_bolson", ["id", "asiento", "create_uid", "name", "diario", "company_id", "create_date", "write_date", "cuenta_desajuste", "write_uid", "fecha", "usuario_id"])
    # cur.execute("select id, asiento, create_uid, name, diario, company_id, create_date, write_date, cuenta_desajuste, write_uid, fecha, usuario_id from bolson_bolson;")
    # for l in cur:
    #     print cur.mogrify("insert into bolson_bolson (id, asiento, create_uid, name, diario, company_id, create_date, write_date, cuenta_desajuste, write_uid, fecha, usuario_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", l)

    update(cur, "account_invoice", ["bolson_id", "id"])
    # cur.execute("select bolson_id, id from account_invoice where bolson_id is not null;")
    # for l in cur:
    #     print cur.mogrify("update account_invoice set bolson_id = %s where id = %s;", l)

    update(cur, "account_payment", ["bolson_id", "id"])
    # cur.execute("select bolson_id, id from account_payment where bolson_id is not null;")
    # for l in cur:
    #     print cur.mogrify("update account_payment set bolson_id = %s where id = %s;", l)

# conciliacion_bancaria
if 0:
    print("delete from conciliacion_bancaria_fecha;")

    insert(cur, "conciliacion_bancaria_fecha", ["id", "create_uid", "create_date", "fecha", "write_uid", "write_date", "move_id"])
    # cur.execute("select id, create_uid, create_date, fecha, write_uid, write_date, move_id from conciliacion_bancaria_fecha;")
    # for l in cur:
    #     print cur.mogrify("insert into conciliacion_bancaria_fecha (id, create_uid, create_date, fecha, write_uid, write_date, move_id) values (%s, %s, %s, %s, %s, %s, %s);", l)

# gface_infile
if 0:
    update(cur, "account_invoice", ["firma_gface", "pdf_gface", "id"])
    # cur.execute("select firma_gface, pdf_gface, id from account_invoice where firma_gface is not null or pdf_gface is not null;")
    # for l in cur:
    #     print cur.mogrify("update account_invoice set firma_gface = %s, pdf_gface = %s where id = %s;", l)

    update(cur, "account_journal", ["usuario_gface", "clave_gface", "nombre_establecimiento_gface", "tipo_documento_gface", "serie_documento_gface", "serie_gface", "numero_resolucion_gface", "fecha_resolucion_gface", "rango_inicial_gface", "rango_final_gface", "numero_establecimiento_gface", "dispositivo_gface", "id"])
    # cur.execute("select usuario_gface, clave_gface, nombre_establecimiento_gface, tipo_documento_gface, serie_documento_gface, serie_gface, numero_resolucion_gface, fecha_resolucion_gface, rango_inicial_gface, rango_final_gface, numero_establecimiento_gface, dispositivo_gface, id from account_journal;")
    # for l in cur:
    #     print cur.mogrify("update account_journal set usuario_gface = %s, clave_gface = %s, nombre_establecimiento_gface = %s, tipo_documento_gface = %s, serie_documento_gface = %s, serie_gface = %s, numero_resolucion_gface = %s, fecha_resolucion_gface = %s, rango_inicial_gface = %s, rango_final_gface = %s, numero_establecimiento_gface = %s, dispositivo_gface = %s where id = %s;", l)

# l10n_gt_extra
if 0:
    update(cur, "account_invoice", ["tipo_gasto", "numero_viejo", "id"])
    # cur.execute("select tipo_gasto, numero_viejo, id from account_invoice;")
    # for l in cur:
    #     print cur.mogrify("update account_invoice set tipo_gasto = %s, numero_viejo = %s where id = %s;", l)

    update(cur, "account_payment", ["numero_viejo", "nombre_impreso", "id"])
    # cur.execute("select numero_viejo, nombre_impreso, id from account_payment;")
    # for l in cur:
    #     print cur.mogrify("update account_payment set numero_viejo = %s, nombre_impreso = %s where id = %s;", l)

    update(cur, "account_journal", ["direccion", "id"])
    # cur.execute("select direccion, id from account_journal;")
    # for l in cur:
    #     print cur.mogrify("update account_journal set direccion = %s where id = %s;", l)

    update(cur, "res_partner", ["pequenio_contribuyente", "id"])
    # cur.execute("select pequenio_contribuyente, id from res_partner;")
    # for l in cur:
    #     print cur.mogrify("update res_partner set pequenio_contribuyente = %s where id = %s;", l)

# pos_gt
if 0:
    print("delete from pos_gt_bom_extra_line;")
    print("delete from pos_gt_extra_line;")
    print("delete from pos_gt_extra;")
    print("delete from pos_gt_extra_product_template_rel;")

    insert(cur, "pos_gt_bom_extra_line", ["id", "name", "product_id", "product_qty", "product_uom_id", "bom_id"])
    # cur.execute("select id, name, product_id, product_qty, product_uom_id, bom_id from pos_gt_bom_extra_line;")
    # for l in cur:
    #     print cur.mogrify("insert into pos_gt_bom_extra_line (id, name, product_id, product_qty, product_uom_id, bom_id) values (%s, %s, %s, %s, %s, %s);", l)

    update(cur, "pos_config", ["allow_discount", "allow_price_change", "ask_tag_number", "takeout_option", "default_client_id", "analytic_account_id", "id"])
    # cur.execute("select allow_discount, allow_price_change, ask_tag_number, takeout_option, default_client_id, analytic_account_id, id from pos_config;")
    # for l in cur:
    #     print cur.mogrify("update pos_config set allow_discount = %s, allow_price_change = %s, ask_tag_number = %s, takeout_option = %s, default_client_id = %s, analytic_account_id = %s where id = %s;", l)

    insert(cur, "pos_gt_extra", ["id", "name", "company_id", "type"])
    # cur.execute("select id, name, company_id, type from pos_gt_extra;")
    # for l in cur:
    #     print cur.mogrify("insert into pos_gt_extra (id, name, company_id, type) values (%s, %s, %s, %s);", l)

    insert(cur, "pos_gt_extra_line", ["id", "name", "extra_id", "product_id", "qty", "price_extra", "company_currency_id"])
    # cur.execute("select id, name, extra_id, product_id, qty, price_extra, company_currency_id from pos_gt_extra_line;")
    # for l in cur:
    #     print cur.mogrify("insert into pos_gt_extra_line (id, name, extra_id, product_id, qty, price_extra, company_currency_id) values (%s, %s, %s, %s, %s, %s, %s);", l)

    insert(cur, "pos_gt_extra_product_template_rel", ["product_template_id", "pos_gt_extra_id"])
    # cur.execute("select product_template_id, pos_gt_extra_id from pos_gt_extra_product_template_rel;")
    # for l in cur:
    #     print cur.mogrify("insert into pos_gt_extra_product_template_rel (product_template_id, pos_gt_extra_id) values (%s, %s);", l)

    update(cur, "res_users", ["default_pos_id", "id"])
    # cur.execute("select default_pos_id, id from res_users;")
    # for l in cur:
    #     print cur.mogrify("update res_users set default_pos_id = %s where id = %s;", l)

# pos_sat
if 0:
    print("delete from pos_gt_extra_product_template_rel;")

    insert(cur, "pos_sat_resolucion", ["id", "name", "fecha", "serie", "direccion", "inicial", "final", "primera", "valido", "tipo_doc", "fecha_ingreso", "fecha_vencimiento"])
    # cur.execute("select id, name, fecha, serie, direccion, inicial, final, primera, valido, tipo_doc, fecha_ingreso, fecha_vencimiento from pos_sat_resolucion;")
    # for l in cur:
    #     print cur.mogrify("insert into pos_sat_resolucion (id, name, fecha, serie, direccion, inicial, final, primera, valido, tipo_doc, fecha_ingreso, fecha_vencimiento) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", l)

    update(cur, "account_journal", ["requiere_resolucion", "ultimo_numero_factura", "id"])
    # cur.execute("select requiere_resolucion, ultimo_numero_factura, id from account_journal;")
    # for l in cur:
    #     print cur.mogrify("update account_journal set requiere_resolucion = %s, ultimo_numero_factura = %s where id = %s;", l)

    update(cur, "ir_sequence", ["resolucion_id", "id"])
    # cur.execute("select resolucion_id, id from ir_sequence;")
    # for l in cur:
    #     print cur.mogrify("update ir_sequence set resolucion_id = %s where id = %s;", l)

    update(cur, "pos_order", ["numero_factura_impreso", "id"])
    # cur.execute("select numero_factura_impreso, id from pos_order;")
    # for l in cur:
    #     print cur.mogrify("update pos_order set numero_factura_impreso = %s where id = %s;", l)

# guateburger
if 1:
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