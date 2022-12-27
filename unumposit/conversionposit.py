import numpy as np

class InvalidPositArgException (Exception):
    pass

class ValueException (Exception):
    pass

class Posit:
    def __init__(self,N=8,es=1):
        self.N=N
        self.exponentBits=es
        self.sign=0
        self.regimeBits=0
        self.binaryFormat="00000000"
        self.decimalFormat=0
        self.regime=0
        self.exponent=0
        self.mantisa=0
        
        if N!=8 and N!=16 and N!=32:
            print("N (number of bit) should be a number between: 8, 16 and 32")
            raise InvalidPositArgException

        if es > N or es<0:
            print("es (number of bits of exponent) should be positive number and smaller than the number of bits N")
            raise InvalidPositArgException

       
        
        
        
    def binaryNum(self,positBinary):
        self.binaryFormat=positBinary
        if (self.binaryFormat[1::].count("0")==self.N-1 and self.binaryFormat[0]=="1"):
            self.decimalFormat=np.inf
            print("It is an exception value of a posit number.")
            raise ValueException

        if (self.binaryFormat[1::].count("0")==self.N-1 and self.binaryFormat[0]=="0"):
            self.decimalFormat=0
            raise ValueException

        if len(self.binaryFormat)!=self.N:
            print("The lenght of the posit number in Binary Format is not correct.")
            raise InvalidPositArgException
        




class BinaryOperations():
    def __init__(self) -> None:
        pass

    def twosComplement(binaryNumber):
        n=len(binaryNumber)
        i = n - 1
        while(i >= 0):
            if (binaryNumber[i] == '1'):
                break
            i -= 1
        if (i == -1):
            return '1'+ binaryNumber
 
        k = i - 1
        while(k >= 0):
            if (binaryNumber[k] == '1'):
                binaryNumber = list(binaryNumber)
                binaryNumber[k] = '0'
                binaryNumber = ''.join(binaryNumber)
            else:
                binaryNumber = list(binaryNumber)
                binaryNumber[k] = '1'
                binaryNumber = ''.join(binaryNumber)
    
            k -= 1

        return binaryNumber  

        

class Conversions():
    def __init__(self) -> None:
        pass

    def float2bin(float_number,num_bits):
        cadena_final=""
        value= str(float_number)
        for i in range(0,num_bits):

            el_punto=value.find(".")
            value_arr= float("0."+value[el_punto+1::])
            result= value_arr*2
            front_point = str(int(result))
            cadena_final=cadena_final+front_point

            el_punto2=(str(result)).find(".")
            value= str("0."+str(result)[el_punto2+1::])

        return cadena_final
    
    def binary_to_decimal(string_binary):
        posicion = 0
        decimal = 0
        string_binary = string_binary[::-1]
        for digito in string_binary:
            # Elevar 2 a la posición actual
            multiplicador = 2**posicion
            decimal += int(digito) * multiplicador
            posicion += 1
        return decimal
    
    def binary_to_significant(string_binary):
        posicion = 1
        significant = 0
        for digito in string_binary:
            # Elevar 2 a la posición actual
            multiplicador = 2**(-1*posicion)
            significant += int(digito) * multiplicador
            posicion += 1
        return significant
   

def sign(decimal):
        if decimal<0 :
            return 1
        else:
            return 0

def decimal_to_posit(decimal,N,es):
    try:
        posit=Posit(N,es)
        
        if decimal==0:
            posit.binaryFormat= "0"*N
        else:
            useed= 2**(2**es)
            maxpos= useed**(N-2)
            minpos= useed**(2-N)

            if abs(decimal)<minpos:
                posit.decimalFormat= minpos
                decimal= minpos
            
            s=sign(decimal)
            posit.sign=s

            decimal_cut=np.clip(abs(decimal), minpos,maxpos)
            logaritmo_dec= np.log2(decimal_cut)
        
            exp=logaritmo_dec
            k=int(np.floor(exp / (2**es)))   


            if (logaritmo_dec<0):
                k=(-1)*(np.ceil(abs(exp / (2**es))))            
            else:
                k=int(np.floor(exp / (2**es)))   

            e=round(np.clip(abs(exp - k* (2**es)), 0, (2**(es))-1))
            

            if k>0:
                rb=k+2
            else:
                rb=-k+1
            

            m=N-1-rb-es
            f= np.clip(abs((decimal_cut/(2**(k* (2**es) +e)) )-1),0,((2**m)-1)/2**m)

            eb= min(N-1-rb,es)
            fb= max(N-1-rb-eb,0)
            pe=(np.floor(e*(2**(eb-es)))) * 2**(es-eb)
            pf=(round(f*(2**fb))) *(2**-fb)


            #Construction binary
            
            #signo is 's'

            #regimen
            regime=""
            if(k<0):
                for i in range(0,abs(int(k))):
                    regime= regime + "0"
                regime= regime +"1"
            else:
                for i in range(0,abs(int(k))+1):
                    regime= regime + "1"
                regime= regime +"0"
            
            posit.regimeBits=len(regime)
            posit.regime=k

            #exponente
            exponente=str(bin(int(abs(pe))))[2::]
            if len(exponente) < es:
                diference=es-len(exponente)
                dif_reg_exp= N-1-len(regime)
                exponente=diference*"0"+exponente
                if (dif_reg_exp==1):
                    exponente=exponente[0]

            
            if len(regime)==(N-1):
                exponente=0*exponente

            #mantissa
            mantissa_bits= N-1-es-len(regime)
            if pf==0:
                mantissa=mantissa_bits*"0"
            else:
                mantissa= str(Conversions.float2bin(pf,mantissa_bits))
            
            #posit number binary
            
            if s==1:
                posit.binaryFormat= str(s) + BinaryOperations.twosComplement(regime + exponente + mantissa)
            else:
                posit.binaryFormat= str(s) + regime + exponente + mantissa
            
            posit.mantisa= 1+ Conversions.binary_to_significant(mantissa)
            posit.exponent=Conversions.binary_to_decimal(exponente)
            posit.decimalFormat = ((-1)**int(s)) *useed**(k) * 2 **Conversions.binary_to_decimal(exponente) * (1+ Conversions.binary_to_significant(mantissa))
            
        #return posit

    except InvalidPositArgException:
        posit=Posit()
        print("There is an exception.")
    finally:
        return posit


def posit_to_decimal(positnum,N,es):
    sum_zeros=0
    sum_ones=0
    posit_shift=0
    regime=0
    exponente=0
    try:
        posit=Posit(N,es)
        posit.binaryNum(positnum)

        #Get sign
        signo= (-1)**int(positnum[0])
        posit.sign=int(positnum[0])
        if (signo<0):
            positnum=BinaryOperations.twosComplement(positnum)
        
        #Get regime
        if(positnum[1]=="0"):
            for i in range(1,N):
                if (positnum[i]=="1"):
                    posit_shift= positnum[i+1:N]
                    posit.regimeBits=i
                    break
                else:
                    sum_zeros+=1
            regime=-1*sum_zeros
        else:
            for i in range(1,N):
                if (positnum[i]=="0"):
                    posit_shift= positnum[i+1:N]
                    posit.regimeBits=i
                    break
                else:
                    sum_ones+=1
            regime=sum_ones-1
        
        posit.regime=regime
        #Get exponent
        exponente = Conversions.binary_to_decimal(posit_shift[0:es])
        posit.exponent=exponente
        
        #Get mantissa
        mantissa_binary = posit_shift[es::]
        mantissa= 1+ Conversions.binary_to_significant(mantissa_binary)
        posit.mantisa=mantissa
        #Get useed
        useed= 2**(2**es)

        #Get decimal number
        posit.decimalFormat= signo * useed**regime * 2**exponente * mantissa


    
    except InvalidPositArgException or ValueException:
        posit=Posit()
        print("There is an exception.")
    
    finally:
        return posit