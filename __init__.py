# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"

    pip install <package> -t .

"""
from win32com import client
import sys
import subprocess
import time

"""
    Obtengo el modulo que fue invocado
"""
module = GetParams("module")
global conx
global id_object

"""
    Realiza Login
"""
if module == "LoginSap":
    # global conx
    # global id_object

    id_user = GetParams('id_user')
    user = GetParams('user')
    id_pass = GetParams('id_pass')
    password = GetParams('password')
    path = GetParams('path')
    conn = GetParams('conn')
    id_button = GetParams('id_btn')

    """
        validaciones
    """
    if not id_user or not id_pass or not conn or not path:
        raise Exception('No ha ingresado todos los datos')

    if id_user:
        try:
            path = path
            subprocess.Popen(path)
            time.sleep(10)

            SapGuiAuto = client.GetObject('SAPGUI')
            application = SapGuiAuto.GetScriptingEngine
            connection = application.OpenConnection(conn, True)
            session = connection.Children(0)

            session.findById(id_user).text = user
            session.findById(id_pass).text = password

            if connection:
                conx = connection

        except:
            PrintException()
            print(sys.exc_info()[0])
            conx = None


if module == "ClickObjeto":
    # global id_object
    id_object = GetParams('id_object')
    tipo = GetParams('tipo')
    #print(id_object)

    if not conx:
        raise Exception("Debe iniciar sesión en SAP")

    try:

        connection = conx
        session = connection.Children(0)
        session.findById("wnd[0]").maximize()

        if id_object:

            if tipo == "text":
                session.findById(id_object).text()

            if tipo == "press":
                session.findById(id_object).press()

            if tipo == "setFocus":
                session.findById(id_object).setFocus()
                print(session.findById(id_object).setFocus())

            if tipo == "select_":
                session.findById(id_object).select()

            if tipo == "close":
                session.findById(id_object).close()

            if tipo == "createSession":
                session.createSession()



    except:
        raise Exception("Debe iniciar sesion en SAP")
        PrintException()


if module == "ExtraerTexto":
    id_object = GetParams('id_object')
    var = GetParams('var')

    try:
        connection = conx
        session = connection.Children(0)

        if id_object:
            val = session.findById(id_object).text
            SetVar(var,val)

    except:
        PrintException()

if module == "click_check":
    id_object = GetParams('id_object')
    tipo = GetParams('tipo')
    # print(id_object)

    if not conx:
        raise Exception("Debe iniciar sesión en SAP")

    try:
        connection = conx
        session = connection.Children(0)
        session.findById("wnd[0]").maximize()

        if id_object and tipo == "marca_":
            session.findById(id_object).selected = -1

        if id_object and tipo == "desmarca_":
            session.findById(id_object).selected = 0

        if not tipo:
            raise Exception("Debe seleccionar una opción")

    except:
        raise Exception("Debe iniciar sesion en SAP")
        PrintException()