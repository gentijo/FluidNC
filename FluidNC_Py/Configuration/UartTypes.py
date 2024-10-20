

from enum import Enum

#MAX_N_UARTS = UART_NUM_MAX;

class UartData(Enum):
    Bits5 = 1 # UART_DATA_5_BITS,
    Bits6 = 2 # UART_DATA_6_BITS,
    Bits7 = 3 # UART_DATA_7_BITS,
    Bits8 = 4 # UART_DATA_8_BITS,


class UartStop(Enum): 
    Bits1   = 1 #UART_STOP_BITS_1,
    Bits1_5 = 2 #UART_STOP_BITS_1_5,
    Bits2   = 3 #UART_STOP_BITS_2,


class UartParity(Enum):
    None = 1 #UART_PARITY_DISABLE,
    Even = 2 #UART_PARITY_EVEN,
    Odd  = 3 #UART_PARITY_ODD,

