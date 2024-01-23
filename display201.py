from guizero import *
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient

    
def update_label():
    
    d=0
    if client.connect():
        request = client.read_input_registers(0,4)
        if not request.isError():
            result = request.registers
            decoder = BinaryPayloadDecoder.fromRegisters(result, Endian.Big, wordorder=Endian.Little)
            d=decoder.decode_32bit_float()

                     
            text.value='{:,.0f}'.format(d)

            if client2.connect():
                #write float
                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                builder.add_32bit_float(d)
                payload = builder.build()
                result  = client2.write_registers(0, payload, skip_encode=True)
            
            
                        
        else:
            text.text_color="red"
            text.value="Err"
      #      client.close()
      #      connection = client.connect()
   
    s=0
    if client.connect():
        request = client.read_input_registers(2,2)
        if not request.isError():
            result = request.registers
            decoder = BinaryPayloadDecoder.fromRegisters(result, Endian.Big, wordorder=Endian.Little)
            s=decoder.decode_16bit_int()
            #texs.value=s #'{:,.0f}'.format(s)
            if client2.connect():
                #write 16b
                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
                builder.add_16bit_int(s)
                payload = builder.build()
                result  = client2.write_registers(2, payload, skip_encode=True)
                         
            if s==4:
                text.text_color="yellow"
                texs.value="CERO CENTRADO"
            else:
                if s==0:
                    text.text_color="#00ff00"
                    texs.value="ESTABLE"
                else:
                    if s==2:
                        text.text_color="red"
                        texs.value="NEGATIVO"
                    else:
                        if s==1:
                            text.text_color="orange"   
                            texs.value="EN MOVIMIENTO"
                        else:
                            text.text_color="white"   
                            texs.value="NoDef-"  + str(s)
        else:
            texs.texr_color="red"
            texs.value="Err"
            client.close()
            connection = client.connect()

    
    # recursive call
    text.after(500, update_label)


if __name__ == '__main__':
    ip_address = "10.1.3.156"
    client = ModbusTcpClient(host=ip_address, port="502", unit=1)
    connection = client.connect()
   
    ip_address2 = "10.1.2.14"
    client2 = ModbusTcpClient(host=ip_address2, port="5020",unit=0)
    connection2 = client2.connect()
    
    app = App(title="Cliente Modbus Conectado a " + ip_address,
              height=700,
              width=2000,
              layout='auto',
              bg="black")

    label1 = Text(app, 'PESO EN PLATAFORMA EN KG:', size=35, color="white")
    label2 = Text(app, ' ', size=29, color="green")
    label3 = Text(app, ' ', size=29, color="green")
#    label4 = Text(app, ' ', size=29, color="green")
    #text = TextBox(app, "xx", width=30, height=40, grid=[1, 0])
    
    text=Text(app,"---",  size=300, color="#00ff00", font="FreeSans Bold")
    texs=Text(app,"---",  size=50, color="#00ff00", font="FreeSans Bold")
    
    text.after(500, update_label)
    
    app.tk.attributes("-fullscreen",True)
    app.display()
