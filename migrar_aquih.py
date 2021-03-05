import sys
import psycopg2

def update(cur, tabla, columnas, where="", tabla_destino=""):
    if not tabla_destino:
        tabla_destino = tabla
            
    columnas_select = ", ".join(columnas)+" as id"
    columnas_update = ", ".join([x+" = %s" for x in columnas[: -1]])

    cur.execute("select {} from {} {}".format(columnas_select, tabla, "where "+where if where else ""))
    for l in cur:
        print(cur.mogrify("update {} set {} where id = %s;".format(tabla_destino, columnas_update), l).decode("utf-8"))

def insert(cur, tabla, columnas, iniciar_seq=True, tabla_destino=""):
    if not tabla_destino:
        tabla_destino = tabla
    
    columnas_select = ", ".join(columnas)
    columnas_insert = ", ".join(["%s" for x in columnas])

    cur.execute("select {} from {}".format(columnas_select, tabla))
    for l in cur:
        print(cur.mogrify("insert into {} ({}) values ({});".format(tabla_destino, columnas_select, columnas_insert), l).decode("utf-8"))

    if iniciar_seq is True:
        print(cur.mogrify("select setval('{}_id_seq', (select max(id) from {})+1);".format(tabla, tabla)).decode("utf-8"))

def update_invoice(cur, columnas):
    columnas_select = ", ".join(columnas)+" as id"
    columnas_update = ", ".join([x+" = %s" for x in columnas[: -1]])

    cur.execute("select {} from {}".format(columnas_select, "account_invoice"))
    for l in cur:
        print(cur.mogrify("update {} set {} where id = %s;".format("account_move", columnas_update), l).decode("utf-8"))

string_conexion = "dbname={} user={} password={} host={} port={}"
dbname = sys.argv[2] if len(sys.argv) > 2 else ""
user = sys.argv[3] if len(sys.argv) > 3 else ""
password = sys.argv[4] if len(sys.argv) > 4 else ""
host = sys.argv[5] if len(sys.argv) > 5 else "localhost"
port = sys.argv[6] if len(sys.argv) > 6 else "5432"
conn = psycopg2.connect(string_conexion.format(dbname, user, password, host, port))
cur = conn.cursor()

# albaran_analitico
if 'albaran_analitico' in sys.argv[1]:
    update(cur, "stock_picking", ["cuenta_analitica_id", "id"], where="cuenta_analitica_id is not null")
    update(cur, "stock_inventory", ["cuenta_analitica_id", "id"], where="cuenta_analitica_id is not null")

# presupuesto_etiquetas
if 'presupuesto_etiquetas' in sys.argv[1]:
    update(cur, "crossovered_budget_lines", ["analytic_tag_id", "id"], where="analytic_tag_id is not null")
    update(cur, "purchase_order_line", ["por_ejecutar", "por_ejecutar_sin_compras", "id"])

# activos
if 'activos' in sys.argv[1]:
    print("delete from activos_localidad;")
    #print("delete from activos_area;")

    insert(cur, "activos_localidad", ["id", "name", "create_date", "write_date", "create_uid", "write_uid"])
    #insert(cur, "activos_area", ["id", "name", "create_date", "write_date", "create_uid", "write_uid"])
    update(cur, "account_asset_asset", ["localidad_id", "responsable_id", "numero_de_serie", "marca", "modelo", "etiqueta", "estado", "id"], tabla_destino="account_asset")

# bolson
if 'bolson' in sys.argv[1]:
    print("update account_move set bolson_id = null from bolson_bolson where bolson_id is not null;")
    print("update account_payment set bolson_id = null from bolson_bolson where bolson_id is not null;")
    print("delete from bolson_bolson;")

    insert(cur, "bolson_bolson", ["id", "asiento", "create_uid", "name", "diario", "company_id", "create_date", "write_date", "cuenta_desajuste", "write_uid", "fecha", "usuario_id"])
    update(cur, "account_invoice", ["bolson_id", "move_id"], tabla_destino="account_move", where="bolson_id is not null")
    update(cur, "account_payment", ["bolson_id", "id"], where="bolson_id is not null")

# conciliacion_bancaria
if 'conciliacion_bancaria' in sys.argv[1]:
    print("delete from conciliacion_bancaria_fecha;")
    print("delete from conciliacion_bancaria_pendientes_excel;")

    insert(cur, "conciliacion_bancaria_fecha", ["id", "create_uid", "create_date", "fecha", "write_uid", "write_date", "move_id"])
    insert(cur, "conciliacion_bancaria_pendientes_excel", ["id", "fecha", "account_id", "tipo_documento", "numero_documento", "monto", "tipo_movimiento", "create_date", "write_date", "create_uid", "write_uid"], tabla_destino="conciliacion_bancaria_pendiente")
    update(cur, "account_journal", ["tipo_movimiento", "id"], where="tipo_movimiento is not null")

# gface_infile
if 'gface_infile' in sys.argv[1]:
    update(cur, "account_invoice", ["firma_gface", "pdf_gface", "move_id"], tabla_destino="account_move", where="firma_gface is not null or pdf_gface is not null")
    #update(cur, "account_journal", ["usuario_gface", "clave_gface", "nombre_establecimiento_gface", "tipo_documento_gface", "serie_documento_gface", "serie_gface", "numero_resolucion_gface", "fecha_resolucion_gface", "rango_inicial_gface", "rango_final_gface", "numero_establecimiento_gface", "dispositivo_gface", "id"])

# gface_guatefactura
if 'gface_guatefactura' in sys.argv[1]:
    update(cur, "account_invoice", ["firma_gface", "nombre_cliente_gface", "direccion_cliente_gface", "move_id"], tabla_destino="account_move", where="firma_gface is not null")

# gface_ecofacturas
if 'gface_ecofacturas' in sys.argv[1]:
    cur.execute("select {} from {}".format("name as ref, move_id", "account_invoice"))
    for l in cur:
        print(cur.mogrify("update {} set {} where id = %s;".format("account_move", "ref = %s"), l).decode("utf-8"))

    #update_invoice(cur, ["firma_gface", "pdf_gface", "move_id"])

# l10n_gt_extra
if 'l10n_gt_extra' in sys.argv[1]:
    update(cur, "account_invoice", ["tipo_gasto", "serie_rango", "inicial_rango", "final_rango", "nota_debito", "move_id"], tabla_destino="account_move")
    update(cur, "account_payment", ["descripcion", "numero_viejo", "nombre_impreso", "no_negociable", "anulado", "fecha_anulacion", "id"])
    update(cur, "account_journal", ["direccion", "codigo_establecimiento", "facturas_por_rangos", "usar_referencia", "id"])
    update(cur, "res_partner", ["pequenio_contribuyente", "cui", "no_validar_nit", "id"])

# pos_gt
if 'pos_gt' in sys.argv[1]:
    #print("delete from pos_gt_bom_extra_line;")
    print("delete from pos_gt_extra_line;")
    print("delete from pos_gt_extra;")
    print("delete from pos_gt_extra_product_template_rel;")

    #insert(cur, "pos_gt_bom_extra_line", ["id", "name", "product_id", "product_qty", "product_uom_id", "bom_id", "create_date", "write_date", "create_uid", "write_uid"])
    update(cur, "pos_config", ["allow_discount", "ask_tag_number", "takeout_option", "default_client_id", "analytic_account_id", "id"])
    insert(cur, "pos_gt_extra", ["id", "name", "company_id", "type", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "pos_gt_extra_line", ["id", "name", "extra_id", "product_id", "qty", "price_extra", "company_currency_id", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "pos_gt_extra_product_template_rel", ["product_template_id", "pos_gt_extra_id"], iniciar_seq=False)
    update(cur, "res_users", ["default_pos_id", "id"])

# pos_sat
if 'pos_sat' in sys.argv[1]:
    insert(cur, "pos_sat_resolucion", ["id", "name", "fecha", "serie", "direccion", "inicial", "final", "primera", "valido", "tipo_doc", "fecha_ingreso", "fecha_vencimiento", "create_date", "write_date", "create_uid", "write_uid"])
    update(cur, "account_journal", ["requiere_resolucion", "ultimo_numero_factura", "id"])
    update(cur, "ir_sequence", ["resolucion_id", "id"])
    update(cur, "pos_order", ["numero_factura_impreso", "id"])

# fel_gt
if 'fel_gt' in sys.argv[1]:
    update(cur, "account_invoice", ["firma_fel", "serie_fel", "numero_fel", "factura_original_id", "consignatario_fel", "comprador_fel", "exportador_fel", "incoterm_fel", "move_id"], tabla_destino="account_move")
    update(cur, "account_journal", ["tipo_documento_fel", "id"])
    update(cur, "res_company", ["frases_fel", "adenda_fel", "id"])

# fel_infile
if 'fel_infile' in sys.argv[1]:
    update(cur, "account_invoice", ["pdf_fel", "move_id"], tabla_destino="account_move", where="pdf_fel is not null")

# importaciones
if 'importaciones' in sys.argv[1]:
    print("delete from account_tax_importaciones_poliza_linea_rel;")
    print("delete from account_invoice_importaciones_poliza_linea_rel;")
    print("delete from importaciones_gasto_asociado_importaciones_poliza_linea_rel;")
    print("delete from importaciones_gasto_asociado;")
    print("delete from importaciones_documento_asociado;")
    print("delete from importaciones_poliza_linea;")
    print("delete from importaciones_poliza;")
    print("delete from importaciones_tipo_gasto;")

    insert(cur, "importaciones_tipo_gasto", ["id", "name", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "importaciones_poliza", ["id", "name", "fecha", "company_id", "poliza_aduana", "tipo_importacion", "guia", "transportista_id", "comentario", "moneda_base_id", "moneda_compra_id", "tasa", "arancel_total", "state", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "importaciones_poliza_linea", ["id", "name", "poliza_id", "producto_id", "pedido", "cantidad", "impuestos_importacion_manual", "impuestos", "precio", "costo_proyectado", "costo", "porcentage_gasto", "porcentage_gasto_importacion", "total_gastos", "total_gastos_importacion", "costo_asignado", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "importaciones_documento_asociado", ["id", "name", "poliza_id", "factura_id", "tipo_gasto_id", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "importaciones_gasto_asociado", ["id", "name", "poliza_id", "valor", "tipo_gasto_id", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "importaciones_gasto_asociado_importaciones_poliza_linea_rel", ["importaciones_poliza_linea_id", "importaciones_gasto_asociado_id"], iniciar_seq=False)
    insert(cur, "account_invoice_importaciones_poliza_linea_rel", ["importaciones_poliza_linea_id", "account_invoice_id"], iniciar_seq=False)
    insert(cur, "account_tax_importaciones_poliza_linea_rel", ["importaciones_poliza_linea_id", "account_tax_id"], iniciar_seq=False)
    update(cur, "purchase_order", ["poliza_id", "gasto_general_poliza", "id"])
    
# rrhh
if 'rrhh' in sys.argv[1]:
    print("delete from hr_salary_rule_rrhh_recibo_linea_rel;")
    print("delete from rrhh_recibo_linea;")
    print("delete from rrhh_recibo;")
    print("delete from rrhh_prestamo_linea;")
    print("delete from rrhh_prestamo;")
    print("delete from hr_salary_rule_rrhh_planilla_columna_rel;")
    print("delete from hr_payslip_input_type_rrhh_planilla_columna_rel;")
    print("delete from rrhh_planilla_columna;")
    print("delete from rrhh_planilla;")
    print("delete from rrhh_entrada_linea;")
    
    update(cur, "account_payment", ["nomina_id", "id"], where="nomina_id is not null")
    update(cur, "hr_payslip_run", ["porcentaje_prestamo", "id"])
    insert(cur, "rrhh_recibo", ["id", "name", "descripcion", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "rrhh_recibo_linea", ["id", "name", "tipo", "sequence", "recibo_id", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "hr_salary_rule_rrhh_recibo_linea_rel", ["rrhh_recibo_linea_id", "hr_salary_rule_id"], iniciar_seq=False)
    update(cur, "hr_contract_type", ["calcula_indemnizacion", "id"])
    update(cur, "hr_contract", ["motivo_terminacion", "base_extra", "fecha_reinicio_labores", "temporalidad_contrato", "calcula_indemnizacion", "id"])
    insert(cur, "rrhh_prestamo", ["id", "employee_id", "fecha_inicio", "numero_descuentos", "total", "mensualidad", "descripcion", "codigo", "estado", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "rrhh_prestamo_linea", ["id", "mes", "monto", "anio", "prestamo_id", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "prestamo_nominda_id_rel", ["rrhh_prestamo_linea_id", "hr_payslip_id"], iniciar_seq=False)
    update(cur, "hr_employee", ["numero_liquidacion", "codigo_centro_trabajo", "codigo_ocupacion", "condicion_laboral", "job_id", "department_id", "diario_pago_id", "igss", "irtra", "nit", "recibo_id", "nivel_academico", "profesion", "etnia", "idioma", "pais_origen", "trabajado_extranjero", "motivo_finalizacion", "jornada_trabajo", "permiso_trabajo", "contacto_emergencia", "marital", "vecindad_dpi", "tarjeta_salud", "tarjeta_manipulacion", "tarjeta_pulmones", "tarjeta_fecha_vencimiento", "codigo_empleado", "departamento_id", "pais_id", "documento_identificacion", "forma_trabajo_extranjero", "pais_trabajo_extranjero_id", "finalizacion_laboral_extranjero", "pueblo_pertenencia", "primer_nombre", "segundo_nombre", "primer_apellido", "segundo_apellido", "apellido_casada", "centro_trabajo_id", "id"])
    insert(cur, "rrhh_planilla", ["id", "name", "descripcion", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "rrhh_planilla_columna", ["id", "name", "sequence", "planilla_id", "sumar", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "hr_salary_rule_rrhh_planilla_columna_rel", ["rrhh_planilla_columna_id", "hr_salary_rule_id"], iniciar_seq=False)
    insert(cur, "hr_rule_input_rrhh_planilla_columna_rel", ["rrhh_planilla_columna_id", "hr_rule_input_id"], iniciar_seq=False)
    insert(cur, "rrhh_entrada_linea", ["id", "input_id", "recibo_id", "create_date", "write_date", "create_uid", "write_uid"])
    update(cur, "res_company", ["version_mensaje", "numero_patronal", "tipo_planilla", "codigo_centro_trabajo", "nombre_centro_trabajo", "direccion_centro_trabajo", "zona_centro_trabajo", "fax", "telefonos", "nombre_contacto", "correo_electronico", "codigo_departamento", "codigo_municipio", "codigo_actividad_economica", "identificacion_tipo_planilla", "nombre_tipo_planilla", "tipo_afiliados", "periodo_planilla", "departamento_republica", "actividad_economica", "clase_planilla", "representante_legal_id", "origen_compania", "barrio_colonia", "nomenclatura", "sindicato", "contratar_personal", "contabilidad_completa", "rango_ingresos", "jefe_recursos_humanos_id", "anio_inicio_operaciones", "tamanio_empresa_ventas", "tamanio_empresa_trabajadores", "actividad_gran_grupo", "sub_actividad_economica", "ocupacion_grupo", "id"])

# pos_gface
if 'pos_gface' in sys.argv[1]:
    pass
    
# pos_guardar
if 'pos_guardar' in sys.argv[1]:
    update(cur, "pos_config", ["save_order_option", "load_order_option", "load_order_session_option", "session_save_order", "opcion_pedidos_vendedor", "id"])

# guateburger
if 'guateburger' in sys.argv[1]:
    print("delete from guateburger_pedido_tienda_linea;")
    print("delete from guateburger_pedido_tienda;")
    print("delete from pos_config_product_category_rel;")

    insert(cur, "guateburger_pedido_tienda", ["id", "name", "fecha", "default_pos_id", "state", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "guateburger_pedido_tienda_linea", ["id", "pedido_tienda_id", "product_id", "uom_po_id", "cantidad", "create_date", "write_date", "create_uid", "write_uid"])
    update(cur, "pos_config", ["tipo_impresora", "id"])
    insert(cur, "pos_config_product_category_rel", ["pos_config_id", "product_category_id"], iniciar_seq=False)
    update(cur, "purchase_order", ["fecha_recepcion_factura", "fecha_pago", "numero_factura", "id"])
    update(cur, "account_invoice", ["fecha_pago", "id"])
    update(cur, "res_partner", ["correo_pagos", "id"])

# grupo2g
if 'grupo2g' in sys.argv[1]:
    print("delete from grupo2g_equivalente_linea;")
    print("delete from grupo2g_linea;")
    print("delete from grupo2g_clasificacion;")
    print("delete from grupo2g_tipo;")
    print("delete from grupo2g_marca;")

    insert(cur, "grupo2g_marca", ["id", "name", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "grupo2g_tipo", ["id", "nombre", "secuencia", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "grupo2g_clasificacion", ["id", "nombre", "secuencia", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "grupo2g_linea", ["id", "producto_id", "ubicacion_id", "localidad", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "grupo2g_equivalente_linea", ["id", "producto_id", "marca", "numero", "actual", "create_date", "write_date", "create_uid", "write_uid"])
    update(cur, "hr_employee", ["descuento_minimo", "descuento_maximo", "comision_minima", "comision_maxima", "id"])
    update(cur, "pos_config", ["search_product_option", "id"])
    update(cur, "product_template", ["codigo_viejo", "marca_id", "tipo", "clasificacion", "secuencia", "venta_tipica", "id"])
    update(cur, "stock_location", ["picking_type_id", "id"])

# donlimon
if 'donlimon' in sys.argv[1]:
    print("delete from donlimon_gastos;")

    insert(cur, "donlimon_gastos", ["id", "product_id", "product_qty", "price_unit", "location_id", "basado_en_cantidades", "create_date", "write_date", "create_uid", "write_uid"])
    update(cur, "account_invoice_line", ["lote_id", "id"])
    update(cur, "product_template", ["brand", "origen", "id"])
    update(cur, "purchase_order", ["venta_origen_id", "compra_origen_id", "id"])
    update(cur, "purchase_order_line", ["lote_id", "id"])
    update(cur, "sale_order", ["calcular_precios", "id"])
    update(cur, "sale_order_line", ["lote_id", "precio_calculado", "precio_base", "diferencia_precio", "id"])
    update(cur, "stock_location", ["proveedor_id", "id"])
    update(cur, "stock_production_lot", ["fecha", "analytic_account_id", "state", "id"])

# fitnessone
if 'fitnessone' in sys.argv[1]:
    print("delete from fitnessone_sincronizacion_programada_linea;")
    print("delete from fitnessone_sincronizacion_programada;")
    print("delete from fitnessone_sede;")
    print("delete from fitnessone_marca;")
    print("delete from fitnessone_pos_motivos_linea;")
    print("delete from fitnessone_pos_motivo;")
    print("delete from reglas_ids_presupuestos_rel;")
    print("delete from fitnessone_presupuesto_nomina_lineas;")
    print("delete from fitnessone_presupuesto_nomina;")
    print("delete from hr_linea_empleado_presupuestado;")
    print("delete from hr_linea_bono_rango;")
    print("delete from hr_linea_entrada_bono;")
    print("delete from hr_entrada_bono;")
    print("delete from hr_linea_bonos;")

    update(cur, "account_journal", ["codigo_jonas", "sucursal", "permitir_extractos", "comision", "id"])
    update(cur, "account_invoice", ["sinc_id", "move_id"], tabla_destino="account_move", where="sinc_id is not null")
    update(cur, "account_invoice_line", ["referencia_pago", "id"], tabla_destino="account_move_line", where="referencia_pago is not null")
    update(cur, "account_analytic_account", ["user_id", "id"], where="user_id is not null")
#    insert(cur, "fitnessone_sincronizacion_programada", ["id", "fecha_carga", "partner_id", "diario_factura_id", "diario_pago_id", "invoice_id", "team_id", "account_analytic_id", "pagar_factura", "barcode", "monto_total", "fecha_procesado", "prioridad", "error", "nota", "create_date", "write_date", "create_uid", "write_uid"])
#    insert(cur, "fitnessone_sincronizacion_programada_linea", ["id", "programada_id", "codigo_producto", "descripcion", "monto", "referencia_pago", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "fitnessone_pos_motivo", ["id", "name", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "fitnessone_pos_motivos_linea", ["id", "departamento", "correo", "journal_id", "motivo_id", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "fitnessone_marca", ["id", "name", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "fitnessone_sede", ["id", "name", "marca_id", "equipo_ventas_id", "stage_id", "plantilla_contabilidad_id", "plantilla_cliente_id", "plantilla_invitacion_id", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "fitnessone_presupuesto_nomina", ["id", "nombre", "responsable_id", "fecha_desde", "fecha_hasta", "company_id", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "fitnessone_presupuesto_nomina_lineas", ["id", "presupuesto_id", "posicion_presupuestaria_id", "cuenta_analitica_id", "departamento_id", "puesto_trabajo_id", "nombre", "fecha_desde", "fecha_hasta", "monto", "company_id", "create_date", "write_date", "create_uid", "write_uid"])
    update(cur, "crm_lead", ["sede_id", "id"])
    insert(cur, "reglas_ids_presupuestos_rel", ["fitnessone_presupuesto_nomina_lineas_id", "hr_salary_rule_id"], iniciar_seq=False)
    update(cur, "hr_employee", ["tipo_discapacidad", "tipo_contrato", "trabajo_especifico", "id"])
    update(cur, "hr_contract", ["horario_trabajo", "forma_jornada", "jornada", "valor_honorarios", "id"])
    insert(cur, "hr_linea_bonos", ["id", "puesto_id", "empleado_id", "cuenta_analitica_id", "mes", "anio", "name", "porcentaje", "rango_inicial", "rango_final", "valor", "calculo_rango", "monto", "codigo", "producto_id", "rangos", "sumar", "active", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "hr_entrada_bono", ["id", "empleado_id", "mes", "anio", "estado", "puesto_id", "tipo", "total", "cuenta_analitica_id", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "hr_linea_entrada_bono", ["id", "entrada_bono_id", "linea_bono_id", "aplica", "porcentaje", "valor", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "hr_linea_bono_rango", ["id", "linea_bono_id", "rango_inicial", "rango_final", "monto", "create_date", "write_date", "create_uid", "write_uid"])
    insert(cur, "hr_linea_empleado_presupuestado", ["id", "puesto_id", "cantidad", "fecha_inicio", "fecha_fin", "cantidad_real", "variacion", "create_date", "write_date", "create_uid", "write_uid"])
    update(cur, "hr_payslip", ["puesto_trabajo_id", "departamento_id", "id"])
    update(cur, "mrp_bom", ["costo_total", "margen_porcentual", "margen", "id"])
    update(cur, "res_partner", ["sinc_id", "genero", "auto_renovacion", "club_id", "club_nombre", "fecha_nacimiento", "contacto_emergencia", "telefono_emergencia", "fecha_expiracion", "nombre_grupo", "numero_grupo", "fecha_ingreso", "fecha_ultima_modificacion", "fecha_miembro_desde", "tipo_miembro", "tipo_membresia", "vendedor_id", "vendedor_nombre", "estado", "estado_fecha_final", "estado_id", "estado_razon", "telefono_trabajo", "id"])
    update(cur, "pos_config", ["habilitar_boton_facturacion", "opcion_comanda", "id"])
    update(cur, "pos_order", ["sinc_id", "motivo_id", "departamento", "correo", "id"])
    update(cur, "purchase_order_line", ["autorizado", "id"])
    update(cur, "purchase_order", ["estado_orden", "nomina_id", "id"])
    update(cur, "sale_order", ["sede_id", "id"])

cur.close()
conn.close()
