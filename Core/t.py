
import sys
from nmmp.nmmp import NMMP_NET, NMMP_Entity


if __name__ == '__main__':

    import timeit
    # import time
    from PyQt5.QtWidgets import QMainWindow, QApplication
    from nmmp.hal.vcom_usart import NUSARTInterface as NUSART

    # create Qt application for correct working QTimer
    qapp = QApplication([])
    ex = QMainWindow()

    # configure HAL for nmmp device
    hal = NUSART(
        name = 'CP210x',
        baudrate = 921600
    )
    hal.logging_on()

    # create NMMP [ Network, Datalink ] layers
    prtcl = NMMP_NET( hal )
    prtcl.logging_on()

    sens_block_0 = NMMP_Entity('Sensor Block 0', 0x00, 0x00000010)
    sens_block_int_temp = NMMP_Entity('SB0 internal temp', 0x01, 0x00000010)
    sens_block_int_vref = NMMP_Entity('SB0 internal vref', 0x02, 0x00000010)

    code = 0x00
    data = 0xEE

    cmd = {
        'get-firmware-id':    [ code, data ],
    }

    progress = 0

    def test():
        global progress

        prtcl.send( sens_block_0, cmd['get-firmware-id'] )
        prtcl.send( sens_block_int_temp, cmd['get-firmware-id'] )

        if progress and progress % 200 == 0:
            print( 'test calls: %s' % (progress*2) )
        progress += 1

    cycles = 4
    cmd_cnt = 2

    t = timeit.timeit( stmt=test, number=cycles )

    # wr_num = cycles * cmd_cnt

    # print( '*'*20 )
    # print( 'send time: %g, single: %.2fms' % (t, (t*1000)/wr_num) )

    # pargs = ( wr_num, prtcl._recivedcnt, wr_num - prtcl._recivedcnt )
    # print( '-'*10, 'send: %g, recived: %g, lost: %g' % pargs )

    ex.show()
    sys.exit(qapp.exec_())


