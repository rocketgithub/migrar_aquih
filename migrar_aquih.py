import sys
import psycopg2

def update(cur, tabla, columnas):
    columnas_select = ", ".join(columnas)
    columnas_update = ", ".join([x+" = %s" for x in columnas[: -1]])

    cur.execute("select {} from {}".format(columnas_select, tabla))
    for l in cur:
        print(cur.mogrify("update {} set {} where id = %s;".format(tabla, columnas_update), l).decode("utf-8"))

def insert(cur, tabla, columnas, iniciar_seq=True):
    columnas_select = ", ".join(columnas)
    columnas_insert = ", ".join(["%s" for x in columnas])

    cur.execute("select {} from {}".format(columnas_select, tabla))
    for l in cur:
        print(cur.mogrify("insert into {} ({}) values ({});".format(tabla, columnas_select, columnas_insert), l).decode("utf-8"))

    if iniciar_seq is True:
        print(cur.mogrify("select setval('{}_id_seq', (select max(id) from {})+1);".format(tabla, tabla)).decode("utf-8"))

def update_invoice(cur, columnas):
    columnas_select = ", ".join(columnas)+" as id"
    columnas_update = ", ".join([x+" = %s" for x in columnas[: -1]])

    cur.execute("select {} from {}".format(columnas_select, "account_invoice"))
    for l in cur:
        print(cur.mogrify("update {} set {} where id = %s;".format("account_move", columnas_update), l).decode("utf-8"))

conn = psycopg2.connect("dbname={} user={}".format(sys.argv[1], sys.argv[2]))
cur = conn.cursor()

# albaran_analitico
if 'albaran_analitico' in sys.argv[3]:
    update(cur, "stock_picking", ["cuenta_analitica_id", "id"])
    update(cur, "stock_inventory", ["cuenta_analitica_id", "id"])

# bolson
if 'bolson' in sys.argv[3]:
    print("update account_move set bolson_id = null from bolson_bolson where bolson_id is not null;")
    print("update account_payment set bolson_id = null from bolson_bolson where bolson_id is not null;")
    print("delete from bolson_bolson;")

    insert(cur, "bolson_bolson", ["id", "asiento", "create_uid", "name", "diario", "company_id", "create_date", "write_date", "cuenta_desajuste", "write_uid", "fecha", "usuario_id"])
    update_invoice(cur, ["bolson_id", "move_id"])
    update(cur, "account_payment", ["bolson_id", "id"])

# conciliacion_bancaria
if 'conciliacion_bancaria' in sys.argv[3]:
    print("delete from conciliacion_bancaria_fecha;")

    insert(cur, "conciliacion_bancaria_fecha", ["id", "create_uid", "create_date", "fecha", "write_uid", "write_date", "move_id"])

# gface_infile
if 'gface_infile' in sys.argv[3]:
    update_invoice(cur, ["firma_gface", "pdf_gface", "move_id"])
    update(cur, "account_journal", ["usuario_gface", "clave_gface", "nombre_establecimiento_gface", "tipo_documento_gface", "serie_documento_gface", "serie_gface", "numero_resolucion_gface", "fecha_resolucion_gface", "rango_inicial_gface", "rango_final_gface", "numero_establecimiento_gface", "dispositivo_gface", "id"])

# gface_ecofacturas
if 'gface_ecofacturas' in sys.argv[3]:
    cur.execute("select {} from {}".format("name as ref, move_id", "account_invoice"))
    for l in cur:
        print(cur.mogrify("update {} set {} where id = %s;".format("account_move", "ref = %s"), l).decode("utf-8"))

    #update_invoice(cur, ["firma_gface", "pdf_gface", "move_id"])

# l10n_gt_extra
if 'l10n_gt_extra' in sys.argv[3]:
    update_invoice(cur, ["tipo_gasto", "move_id"])
    update(cur, "account_payment", ["numero_viejo", "nombre_impreso", "id"])
    update(cur, "account_journal", ["direccion", "id"])
    update(cur, "res_partner", ["pequenio_contribuyente", "cui", "no_validar_nit", "id"])

# pos_gt
if 'pos_gt' in sys.argv[3]:
    print("delete from pos_gt_bom_extra_line;")
    print("delete from pos_gt_extra_line;")
    print("delete from pos_gt_extra;")
    print("delete from pos_gt_extra_product_template_rel;")

    insert(cur, "pos_gt_bom_extra_line", ["id", "name", "product_id", "product_qty", "product_uom_id", "bom_id"])
    update(cur, "pos_config", ["allow_discount", "allow_price_change", "ask_tag_number", "takeout_option", "default_client_id", "analytic_account_id", "id"])
    insert(cur, "pos_gt_extra", ["id", "name", "company_id", "type"])
    insert(cur, "pos_gt_extra_line", ["id", "name", "extra_id", "product_id", "qty", "price_extra", "company_currency_id"])
    insert(cur, "pos_gt_extra_product_template_rel", ["product_template_id", "pos_gt_extra_id"], iniciar_seq=False)
    update(cur, "res_users", ["default_pos_id", "id"])

# pos_sat
if 'pos_sat' in sys.argv[3]:
    insert(cur, "pos_sat_resolucion", ["id", "name", "fecha", "serie", "direccion", "inicial", "final", "primera", "valido", "tipo_doc", "fecha_ingreso", "fecha_vencimiento"])
    update(cur, "account_journal", ["requiere_resolucion", "ultimo_numero_factura", "id"])
    update(cur, "ir_sequence", ["resolucion_id", "id"])
    update(cur, "pos_order", ["numero_factura_impreso", "id"])

# fel_gt
if 'fel_gt' in sys.argv[3]:
    update_invoice(cur, ["firma_fel", "serie_fel", "numero_fel", "factura_original_id", "consignatario_fel", "comprador_fel", "exportador_fel", "incoterm_fel", "move_id"])
    update(cur, "account_journal", ["tipo_documento_fel", "id"])
    update(cur, "res_company", ["frases_fel", "adenda_fel", "id"])

# fel_infile
if 'fel_infile' in sys.argv[3]:
    update_invoice(cur, ["pdf_fel", "move_id"])

# importaciones
if 'importaciones' in sys.argv[3]:
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
    insert(cur, "importaciones_gasto_asociado_importaciones_poliza_linea_rel", ["importaciones_poliza_linea_id", "importaciones_gasto_asociado_id"], iniciar_seq=False)
    insert(cur, "account_invoice_importaciones_poliza_linea_rel", ["importaciones_poliza_linea_id", "account_invoice_id"], iniciar_seq=False)
    insert(cur, "account_tax_importaciones_poliza_linea_rel", ["importaciones_poliza_linea_id", "account_tax_id"], iniciar_seq=False)
    update(cur, "purchase_order", ["poliza_id", "gasto_general_poliza", "id"])
    
# rrhh
if 'rrhh' in sys.argv[3]:
    print("delete from hr_salary_rule_rrhh_recibo_linea_rel;")
    print("delete from rrhh_entrada_linea;")
    print("delete from rrhh_recibo_linea;")
    print("delete from rrhh_recibo;")
    print("delete from rrhh_prestamo_linea")
    print("delete from rrhh_prestamo")
    print("delete from hr_salary_rule_rrhh_planilla_columna_rel;")
    print("delete from hr_rule_input_rrhh_planilla_columna_rel;")
    print("delete from rrhh_planilla_columna;")
    print("delete from rrhh_planilla;")
    
    update(cur, "account_payment", ["nomina_id", "id"])
    update(cur, "hr_payslip_run", ["porcentaje_prestamo", "id"])
    insert(cur, "rrhh_recibo", ["id", "name", "descripcion"])
    insert(cur, "rrhh_recibo_linea", ["id", "name", "tipo", "sequence", "recibo_id"])
    insert(cur, "hr_salary_rule_rrhh_recibo_linea_rel", ["rrhh_recibo_linea_id", "hr_salary_rule_id"], iniciar_seq=False)
    update(cur, "hr_contract_type", ["calcula_indemnizacion", "id"])
    update(cur, "hr_contract", ["motivo_terminacion", "base_extra", "fecha_reinicio_labores", "temporalidad_contrato", "calcula_indemnizacion", "id"])
    insert(cur, "rrhh_prestamo", ["employee_id", "fecha_inicio", "numero_descuentos", "total", "mensualidad", "descripcion", "codigo", "estado"])
    insert(cur, "rrhh_prestamo_linea", ["mes", "monto", "anio", "nomina_id", "prestamo_id"])
    update(cur, "hr_employee", ["numero_liquidacion", "codigo_centro_trabajo", "codigo_ocupacion", "condicion_laboral", "job_id", "department_id", "diario_pago_id", "igss", "irtra", "nit", "recibo_id", "nivel_academico", "profesion", "etnia", "idioma", "pais_origen", "trabajado_extranjero", "motivo_finalizacion", "jornada_trabajo", "permiso_trabajo", "contacto_emergencia", "marital", "vecindad_dpi", "tarjeta_salud", "tarjeta_manipulacion", "tarjeta_pulmones", "tarjeta_fecha_vencimiento", "codigo_empleado", "departamento_id", "pais_id", "documento_identificacion", "forma_trabajo_extranjero", "pais_trabajo_extranjero_id", "finalizacion_laboral_extranjero", "pueblo_pertenencia", "primer_nombre", "segundo_nombre", "primer_apellido", "segundo_apellido", "apellido_casada", "centro_trabajo_id", "id"])
    insert(cur, "rrhh_planilla", ["id", "name", "descripcion"])
    insert(cur, "rrhh_planilla_columna", ["id", "name", "sequence", "planilla_id", "sumar"])
    insert(cur, "hr_salary_rule_rrhh_planilla_columna_rel", ["rrhh_planilla_columna_id", "hr_salary_rule_id"], iniciar_seq=False)
    insert(cur, "hr_rule_input_rrhh_planilla_columna_rel", ["rrhh_planilla_columna_id", "hr_rule_input_id"], iniciar_seq=False)
    insert(cur, "rrhh_entrada_linea", ["id", "input_id", "recibo_id"])
    update(cur, "res_company", ["version_mensaje", "numero_patronal", "tipo_planilla", "codigo_centro_trabajo", "nombre_centro_trabajo", "direccion_centro_trabajo", "zona_centro_trabajo", "fax", "telefonos", "nombre_contacto", "correo_electronico", "codigo_departamento", "codigo_municipio", "codigo_actividad_economica", "identificacion_tipo_planilla", "nombre_tipo_planilla", "tipo_afiliados", "periodo_planilla", "departamento_republica", "actividad_economica", "clase_planilla", "representante_legal_id", "origen_compania", "barrio_colonia", "nomenclatura", "sindicato", "contratar_personal", "contabilidad_completa", "rango_ingresos", "jefe_recursos_humanos_id", "anio_inicio_operaciones", "tamanio_empresa_ventas", "tamanio_empresa_trabajadores", "actividad_gran_grupo", "sub_actividad_economica", "ocupacion_grupo", "id"])

# pos_gface
if 'pos_gface' in sys.argv[3]:
    pass
    
# pos_guardar
if 'pos_guardar' in sys.argv[3]:
    update(cur, "pos_config", ["save_order_option", "load_order_option", "load_order_session_option", "session_save_order", "opcion_pedidos_vendedor", "id"])

# guateburger
if 'guateburger' in sys.argv[3]:
    print("delete from guateburger_pedido_tienda_linea;")
    print("delete from guateburger_pedido_tienda;")
    print("delete from pos_config_product_category_rel;")

    insert(cur, "guateburger_pedido_tienda", ["id", "name", "fecha", "default_pos_id", "state"])
    insert(cur, "guateburger_pedido_tienda_linea", ["id", "pedido_tienda_id", "product_id", "uom_po_id", "cantidad"])
    update(cur, "pos_config", ["tipo_impresora", "id"])
    insert(cur, "pos_config_product_category_rel", ["pos_config_id", "product_category_id"], iniciar_seq=False)
    update(cur, "purchase_order", ["fecha_recepcion_factura", "fecha_pago", "numero_factura", "id"])
    update(cur, "account_invoice", ["fecha_pago", "id"])
    update(cur, "res_partner", ["correo_pagos", "id"])

# grupo2g
if 'grupo2g' in sys.argv[3]:
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
    update(cur, "product_template", ["codigo_viejo", "marca_id", "tipo", "clasificacion", "secuencia", "venta_tipica", "id"])
    update(cur, "stock_location", ["picking_type_id", "id"])

# donlimon
if 'donlimon' in sys.argv[3]:
    print("delete from donlimon_gastos;")

    insert(cur, "donlimon_gastos", ["product_id", "product_qty", "price_unit", "location_id", "basado_en_cantidades"])
    update(cur, "account_invoice_line", ["lote_id", "id"])
    update(cur, "product_template", ["brand", "origen", "id"])
    update(cur, "purchase_order", ["venta_origen_id", "compra_origen_id", "id"])
    update(cur, "purchase_order_line", ["lote_id", "id"])
    update(cur, "sale_order", ["calcular_precios", "id"])
    update(cur, "sale_order_line", ["lote_id", "precio_calculado", "precio_base", "diferencia_precio", "id"])
    update(cur, "stock_location", ["proveedor_id", "id"])
    update(cur, "stock_production_lot", ["fecha", "analytic_account_id", "state", "id"])

cur.close()
conn.close()
