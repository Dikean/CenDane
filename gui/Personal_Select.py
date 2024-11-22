import customtkinter
import tkinter as tk  # Importar Canvas y Scrollbar de tkinter
from customtkinter import CTkComboBox
from Connect_Firebase import ref  # Importar la referencia de la base de datos desde el archivo de conexión
import sys
import os
sys.path.insert(0, os.path.abspath('..'))  # Agrega el directorio padre al path

from models.Cuadro_control import DatabaseManager

db_manager = DatabaseManager()

def get_personal_select_frame(parent):
    # Crear el marco principalF
    personal_frame = customtkinter.CTkFrame(master=parent, corner_radius=0)

    # Configurar las columnas para distribuir las tarjetas
    personal_frame.columnconfigure(0, weight=1)  # Columna 1 con peso 1 (1/4)
    personal_frame.columnconfigure(1, weight=3)  # Columna 2 con peso 3 (3/4)

    # Crear tarjeta para toda la parte superior, ocupando el ancho completo
    card_3 = customtkinter.CTkFrame(master=personal_frame, corner_radius=15, border_width=2)
    card_3.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")  # Ocupa ambas columnas

    # Crear botones dentro de card_3
    button_izquierda = customtkinter.CTkLabel(
        master=card_3, text="Personal Seleccionado",
        fg_color="transparent",  # Ajusta el color de fondo si es necesario
        text_color="white",  # Cambia al color de texto deseado
        font=("Roboto", 18)   # Ajusta la fuente y tamaño según necesites
    )
    button_izquierda.pack(side="left", padx=10, pady=10)


    button_derecha = customtkinter.CTkButton(
        master=card_3, text="AÑADIR", command=lambda: abrir_ventana_añadir(),
        fg_color="transparent", hover_color="gray"
    )
    button_derecha.pack(side="right", padx=10, pady=10)

    button_atrasados = customtkinter.CTkButton(
        master=card_3, text="Enviar Atrasados", command=lambda: enviar_atrasados(),
        fg_color="transparent", hover_color="gray"
    )
    button_atrasados.pack(side="left", padx=10, pady=10)

    # Crear tarjeta para la primera columna con tamaño fijo
    card_1 = customtkinter.CTkFrame(master=personal_frame, corner_radius=15, border_width=2, width=200, height=200)
    card_1.grid_propagate(False)
    card_1.grid(row=1, column=0, padx=10, pady=20, sticky="nsew")

    # Tarjeta derecha (card_2_container) con scroll
    # Tarjeta derecha (card_2_container) con scroll
    card_2_container = customtkinter.CTkFrame(master=personal_frame, corner_radius=15, border_width=2)
    card_2_container.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    # Agregar un CTkScrollableFrame dentro de card_2_container
    scrollable_frame = customtkinter.CTkScrollableFrame(master=card_2_container, width=500, height=400, corner_radius=0)
    scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Configuración del grid dentro de scrollable_frame
    scrollable_frame.columnconfigure(0, weight=1)
    scrollable_frame.columnconfigure(1, weight=1)

    labels = [ "PROYECTO:", "ESTADO_DE_DOCUMENTACION:",
               "SEDE:", "CEDULA_BUSCAR:", "SOLICITUD_DE_DOCUMENTOS:", "FECHA_Y_HORA_DE_ENTREGA_DE_DOCUMENTOS:", "FECHA_DE_INICIO_DEL_OPERAT:", "RESPONSABLE_REVISION:", "ESTADO", "TIPO_DE_CONTRATACION:", "REQUIERE_GARANTIAS:",
               "DIRECCION_TERRITORIAL", "TIPO_DE_CONTRATO_NUEVO_CESION",	"TIPO_DE_CONTRATO",	"PERFIL",	"TIPO_DE_DOCUMENTO_DEL_SUPERVISOR",
               "SUPERVISOR", "CC_SUPERVISOR",	"FECHA_DE_SUSCRIPCION_DEL_CONTRATO",	"FECHA_DE_INICIO_DEL_CONTRATO",	"FECHA_DE_FINALIZACION_DEL_CONTRATO",	"NUMERO_CDP",	"NUMERO_REGISTRO_PRESUPUESTAL",	 "FECHA_INICIO_COBERTURA_A_ARL",	"PROFESION_OBLIGA_TARJETA_PROFESIONAL",	"FECHA_NOTIFICACION_AL_SUPERVISOR",	"FECHA_DE_CARGUE_DE_DOCUMENTOS_ARL_RP_OA_POLIZA",	"FECHA_AFILIACION_ARL",	"FECHA_REGISTRO_DEL_CONTRATO_EN_EL_SIGEP_II",	"FUNCIONARIO_QUIEN_VALIDO_LA_HV_EN_SIGEP_II",	"CEDULA_DEL_FUNCIONARIO_QUE_VALIDO_LA_HV_EN_SIGEP_II",
               "ENTIDAD_DE_SALUD", "ENTIDAD_PENSION",	"ARL",	"FECHA_NACIMIENTO",	"Plazo Ejecución",	"Fecha Inicio", "Fecha Final",	"Valor Honorarios Mensuales",	"Sexo",	"RH",	"Ciudad domicilio",
               "Dirección",	"No. Celular",	"Email personal",	"Maximo nivel de educacion",	"Disciplina o Profesión",	"PROFESIÓN OBLIGA TARJETA PROFESIONAL  (SI / NO)",	"Nacionalidad",	"Departamento de nacimiento",	"MUNICIPIO DE NACIMIENTO",
               "Estado Civil",	"No. De hijos",	"Indique si la Persona ha Tenido Otro Contrato o VinculaciOn en la Presente Vigencia",	"Cuenta con algún tipo de discapacidad",	"Tipo de discapacidad",	"GRUPO ETNICO",	"LINK SECOP II", 
               "NO. LINK", "FECHA NOTIFICACIÓN AL SUPERVISOR2",	"FECHA DE CARGUE DE DOCUMENTOS (ARL + RP + OA POLIZA C/A)3",	"FECHA AFILIACIÓN ARL DIA/MES/AÑO",	"FECHA VINCIULACIÓN AL SIGEP II",	"Funcionario Quien Validó la HV en SIGEP II4",	"Cédula del Funcionario que Validó la HV en SIGEP II5"
             ]
    

    entries = []

    # Suponiendo que estás en el bucle donde creas los campos:
    for i, label_text in enumerate(labels):
        col = i % 2  # Determina la columna
        row = i // 2 * 2  # Multiplica por 2 para dejar espacio entre label y entrada

        label = customtkinter.CTkLabel(master=scrollable_frame, text=label_text, font=("Arial", 14))
        label.grid(row=row, column=col, padx=10, pady=(10, 2), sticky="w")

        if label_text == "ESTADO_DE_DOCUMENTACION:":
            # Crear un ComboBox para el estado de documentación
            estado_doc_values = ["Completo", "Incompleto"]
            entry = CTkComboBox(master=scrollable_frame, values=estado_doc_values)
            # Configurar el valor inicial (ejemplo, se podría ajustar basado en los datos cargados)
            entry.set("Incompleto")
        else:
            entry = customtkinter.CTkEntry(master=scrollable_frame)

        entry.grid(row=row + 1, column=col, padx=10, pady=(2, 10), sticky="ew")
        entries.append(entry)


    # Botones debajo de los inputs
    button_frame = customtkinter.CTkFrame(master=scrollable_frame, fg_color="transparent")
    button_frame.grid(row=len(labels) * 2, column=0, columnspan=2, pady=(10, 10), sticky="e")

    button_guardar = customtkinter.CTkButton(master=button_frame, text="Guardar", command=lambda: print("Borrar usuario"))
    button_guardar.pack(side="right", padx=10)

    button_borrar = customtkinter.CTkButton(master=button_frame, text="Borrar", command=lambda: print("Borrar usuario"))
    button_borrar.pack(side="right", padx=10)


    # Función para mostrar detalles del usuario seleccionado
    def mostrar_detalles(usuario_id, datos):
        for i, label in enumerate(labels):
            key = label[:-1].strip().replace(' ', '_').upper()
            entry = entries[i]
            if isinstance(entry, customtkinter.CTkComboBox):
                entry.set(datos.get(key, 'Incompleto'))
            else:
                entry.delete(0, "end")
                entry.insert(0, datos.get(key, ''))


    # Función para actualizar los datos desde Firebase
    def actualizar_datos():
        usuarios_data = ref.get()  # Obtener todos los datos de 'usuarios'

        # Limpiar la tarjeta `card_1` antes de volver a agregar los botones y entrada
        for widget in card_1.winfo_children():
            widget.destroy()

        # Crear nuevo campo de entrada en la parte superior de `card_1`
        input_entry = customtkinter.CTkEntry(master=card_1, corner_radius=15, placeholder_text="Buscar usuario...", width=300)
        input_entry.pack(padx=10, pady=(15, 10))  # Padding superior e inferior para separarlo del borde

        # Frame para contener los botones horizontalmente (sin fondo)
        buttons_frame = customtkinter.CTkFrame(master=card_1, fg_color="transparent")
        buttons_frame.pack(pady=(5, 10))  # Empaquetar con padding para centrar los botones

        # Crear los cuatro botones con `corner_radius` de 35 píxeles y alinearlos horizontalmente
        font_settings = ("Arial", 9)  # Tamaño de fuente más pequeño
        button_proyecto = customtkinter.CTkButton(master=buttons_frame, text="PROYECTO", corner_radius=35, width=60, font=font_settings, command=lambda: mostrar_submenu("PROYECTO"))
        button_proyecto.grid(row=0, column=0, padx=5, pady=4)

        button_cedula = customtkinter.CTkButton(master=buttons_frame, text="CEDULA", corner_radius=35, width=60, font=font_settings, command=lambda: mostrar_submenu("CEDULA"))
        button_cedula.grid(row=0, column=1, padx=5, pady=4)

        button_name = customtkinter.CTkButton(master=buttons_frame, text="NAME", corner_radius=35, width=60, font=font_settings, command=lambda: mostrar_submenu("NAME"))
        button_name.grid(row=0, column=2, padx=5, pady=4)

        button_responsable = customtkinter.CTkButton(master=buttons_frame, text="RESPONSABLE", corner_radius=35, width=60, font=font_settings, command=lambda: mostrar_submenu("RESPONSABLE"))
        button_responsable.grid(row=0, column=3, padx=5, pady=4)

    
        if usuarios_data:
          for idx, (key, value) in enumerate(usuarios_data.items()):
            cedula = value.get('CEDULA_BUSCAR', 'Desconocido')
            proyecto = value.get('PROYECTO', 'Sin Proyecto')

            # Crear un frame para contener la cédula, el nombre del proyecto y el botón
            user_frame = customtkinter.CTkFrame(master=card_1, fg_color="transparent")
            user_frame.pack(padx=10, pady=5, fill="x")

            # Crear un sub-frame para alinear la cédula y el proyecto verticalmente
            info_frame = customtkinter.CTkFrame(master=user_frame, fg_color="transparent")
            info_frame.pack(side="left", padx=(0, 10), fill="both")

            # Mostrar la cédula
            label_cedula = customtkinter.CTkLabel(master=info_frame, text=f"Cédula: {cedula}", font=("Arial", 12))
            label_cedula.pack(anchor="w")

            # Mostrar el nombre del proyecto debajo de la cédula
            label_proyecto = customtkinter.CTkLabel(master=info_frame, text=f"Proyecto: {proyecto}", font=("Arial", 10))
            label_proyecto.pack(anchor="w")

            # Botón para seleccionar el usuario, con diseño de flecha y tamaño más pequeño
            user_button = customtkinter.CTkButton(
                master=user_frame,
                text="→",
                font=("Arial", 8),
                width=40,  # Ajustar el ancho según sea necesario
                height=25,  # Ajustar la altura según sea necesario
                command=lambda k=key, v=value: mostrar_detalles(k, v)
            )
            user_button.pack(side="right", padx=5)


      
        # Llamar a `actualizar_datos` cada 5 minutos
        personal_frame.after(300000, actualizar_datos)

    # Llamar por primera vez para cargar los datos
    actualizar_datos()

    # Función para borrar un usuario de Firebase
    def borrar_usuario():
        if hasattr(card_2, 'usuario_id'):
            try:
                ref.child(card_2.usuario_id).delete()
                entry_nombre.delete(0, "end")
                entry_correo.delete(0, "end")
                entry_cedula.delete(0, "end")
                actualizar_datos()  # Actualizar los datos después de eliminar
            except Exception as e:
                print(f"Error al borrar usuario: {e}")

    # Función para guardar los cambios de un usuario
    def guardar_usuario():
        # Asegúrate de que existe el identificador del usuario para actualizar los datos.
        if hasattr(card_2_container, 'usuario_id'):
            datos_actualizados = {}
            # Recorrer todos los labels y entries asociados para recolectar los datos.
            for i, label in enumerate(labels):
                key = label[:-1].strip().replace(' ', '_').upper()  # Formatear la clave adecuadamente.
                entry = entries[i]
                if isinstance(entry, CTkComboBox):
                    # Si el elemento es un ComboBox, obtener el valor seleccionado.
                    value = entry.get()
                else:
                    # De lo contrario, simplemente obtener el valor del campo de texto.
                    value = entry.get()
                datos_actualizados[key] = value
            
            # Intentar actualizar los datos en Firebase.
            try:
                ref.child(card_2_container.usuario_id).update(datos_actualizados)  # Utilizar update en lugar de set para modificar.
                print("Datos del usuario actualizados correctamente.")
                actualizar_datos()  # Actualizar la interfaz o datos mostrados si es necesario.
            except Exception as e:
                print(f"Error al guardar usuario: {e}")
        else:
            print("No se pudo encontrar el identificador del usuario para guardar los cambios.")


   
    # Función para abrir la ventana emergente y añadir un usuario
    def abrir_ventana_añadir():
        ventana_añadir = customtkinter.CTkToplevel(personal_frame)
        ventana_añadir.title("Añadir Usuario")
        ventana_añadir.geometry("500x500")

        label_cedula = customtkinter.CTkLabel(ventana_añadir, text="Cédula:", font=("Arial", 14))
        label_cedula.pack(pady=(10, 5))
        entry_cedula = customtkinter.CTkEntry(ventana_añadir)
        entry_cedula.pack(pady=(0, 10))

        label_proyecto = customtkinter.CTkLabel(ventana_añadir, text="Proyecto:", font=("Arial", 14))
        label_proyecto.pack(pady=(10, 5))
        entry_proyecto = customtkinter.CTkEntry(ventana_añadir)
        entry_proyecto.pack(pady=(0, 10))

        label_estado_documentacion = customtkinter.CTkLabel(ventana_añadir, text="Estado de Documentación:", font=("Arial", 14))
        label_estado_documentacion.pack(pady=(10, 5))
        entry_estado_documentacion = customtkinter.CTkEntry(ventana_añadir)
        entry_estado_documentacion.pack(pady=(0, 10))

        label_sede = customtkinter.CTkLabel(ventana_añadir, text="Sede:", font=("Arial", 14))
        label_sede.pack(pady=(10, 5))
        entry_sede = customtkinter.CTkEntry(ventana_añadir)
        entry_sede.pack(pady=(0, 10))

        label_solicitud_documentos = customtkinter.CTkLabel(ventana_añadir, text="Solicitud de Documentos:", font=("Arial", 14))
        label_solicitud_documentos.pack(pady=(10, 5))
        entry_solicitud_documentos = customtkinter.CTkEntry(master=ventana_añadir)
        entry_solicitud_documentos.pack(pady=(0, 10))

        label_responsable_revision = customtkinter.CTkLabel(ventana_añadir, text="Responsable de Revisión:", font=("Arial", 14))
        label_responsable_revision.pack(pady=(10, 5))
        entry_responsable_revision = customtkinter.CTkEntry(ventana_añadir)
        entry_responsable_revision.pack(pady=(0, 20))


        # Botón para enviar los datos a Firebase
        button_enviar = customtkinter.CTkButton(
            ventana_añadir,
            text="Enviar",
            command=lambda: enviar_datos(entry_cedula.get(), entry_proyecto.get(), entry_estado_documentacion.get(), entry_sede.get(), entry_solicitud_documentos.get(), entry_responsable_revision.get() )
        )
        button_enviar.pack(pady=20)

    # Función para enviar los datos a Firebase
    def enviar_datos(cedula, proyecto, estado_documentacion, sede, solicitud_documentos, responsable_revision):
        if cedula and proyecto and estado_documentacion and sede and solicitud_documentos and responsable_revision:
            try:
                nuevo_usuario = {
                    'PROYECTO': proyecto,
                    'ESTADO_DE_DOCUMENTACION': estado_documentacion,
                    'SEDE': sede,
                    'SOLICITUD_DE_DOCUMENTOS': solicitud_documentos,
                    'RESPONSABLE_REVISION': responsable_revision,
                    'CEDULA_BUSCAR': cedula
                }
                ref.push(nuevo_usuario)  # Agregar el nuevo usuario a Firebase
                actualizar_datos()  # Actualizar los datos para reflejar el nuevo usuario
            except Exception as e:
                print(f"Error al añadir usuario: {e}")

    # Función para mostrar un submenú (ejemplo para los botones)
    def mostrar_submenu(opcion):
        print(f"Submenú para: {opcion}")
        # Aquí puedes añadir lógica para mostrar un submenú específico para cada botón

    def enviar_atrasados():
        print("Implementar la lógica para enviar notificaciones a usuarios atrasados.")
        db_manager.fetch_data_greater_than('Atrasado', 2)
        # Aquí puedes agregar la lógica para buscar en la base de datos y enviar correos a los usuarios atrasados


    return personal_frame
