#coding=utf-8
from ctypes import *  
  
#define struct  
class NLU_Input_C_TMP(Structure):  
    _fields_ = [  
        ("ctx_tag", c_char_p),  
        ("tokens", c_char_p),   
        ("topic_note", c_char_p)  
               ]  
    def __init__(self):
        self.ctx_tag = cast(create_string_buffer(100),c_char_p) #create buffer, convert to char* type
        self.tokens_len = 10
        self.tokens = cast(create_string_buffer(1000),c_char_p)
        self.topic_note = cast(create_string_buffer(1000),c_char_p)


class NLU_Result_C_TMP(Structure):  
    _fields_ = [  
        ("domain_text", c_char_p),  
        ("domain_score", c_double),  
        ("slot_values", c_char_p),  
        ("slot_size", c_uint),
        ("pLen", POINTER(c_uint)),
        ("slot_score", c_double),
        ("utterance", c_char_p)
               ]  
    def __init__(self):
        self.domain_text = cast(create_string_buffer(1000),c_char_p)
        self.domain_score = 0.0
        self.slot_values = cast(create_string_buffer(1000),c_char_p)
        self.pLen = (c_uint * 50)()
        self.slot_size = 0
        self.slot_score = 0.0
        self.utterance = cast(create_string_buffer(1000),c_char_p)
        
def ENLU_init(dll, model_file, mode):
    init = dll.ENLU_Init
    init.argtypes = [c_char_p, c_uint]
    init.restype = c_uint
    mode = c_uint(1)
    pModel = c_char_p(model_file)
    #pModel.value = model_file
    init(pModel, mode)

def ENLU_Uninit(dll):
    uninit = dll.ENLU_Uninit
    uninit.argtypes = None
    uninit.restype=c_uint
    uninit()

def ENLU_Classify(dll, inputStruct, outputStruct):
    classifyRes = ""
    classify = dll.ENLU_Classify
    classify.argtypes = [POINTER(NLU_Input_C_TMP), POINTER(NLU_Result_C_TMP)]
    classify.restype = c_uint
    classify(inputStruct, outputStruct)
    classifyRes += outputStruct.domain_text
    return classifyRes
    
def ENLU_Extract(dll, inputStruct, outputStruct):
    slotRes = {}
    extract=dll.ENLU_ExtractWithoutClassify
    extract.argtypes = [POINTER(NLU_Input_C_TMP), POINTER(NLU_Result_C_TMP)]
    extract.restype = c_uint
    extract(inputStruct, outputStruct)
    start = 0
    end = len = outputStruct.pLen[0]
    id = 0
    slotSize = outputStruct.slot_size
    slotContent = ""
    while id < slotSize:
        slotValue = outputStruct.slot_values[start:end - 1]
        slotContent += slotValue + ";"
        domain, name = slotValue.split('=')
        slotRes[name] = domain
        start = end
        id = id + 1
        if id < outputStruct.slot_size:
            end = end + outputStruct.pLen[id]

    return slotRes
    
    
def ENLU_batchProcess(dll, inputFile, outputFile):
    inputStream = open(inputFile, 'rb')
    outputFile = open(outputFile, 'wb')
    resultRes = ""
    for line in inputStream:
        sentence = line.strip()
        outputFile.write(sentence + "\t")
        inputStruct = NLU_Input_C_TMP()
        inputStruct.ctx_tag = "res_type_NCS"
        inputStruct.tokens = sentence#c_char_p(sentence)
        outputStruct = NLU_Result_C_TMP()
        classifyRes = ENLU_Classify(dll, inputStruct, outputStruct)
        slotRes = ENLU_Extract(dll, inputStruct, outputStruct)
        resultRes = classifyRes + "#" + slotRes
        outputFile.write(resultRes + "\n")
    inputStream.close()
    outputFile.close()
    return resultRes


def ENLU_Process(dll, words):
    inputStruct = NLU_Input_C_TMP()
    inputStruct.ctx_tag = "res_type_NCS"
    inputStruct.tokens = words
    outputStruct = NLU_Result_C_TMP()
    classifyRes = ENLU_Classify(dll, inputStruct, outputStruct)
    slotRes = ENLU_Extract(dll, inputStruct, outputStruct)

    return {'domain': classifyRes, 'slot': slotRes}
    
    
def Word_segment_init(dll, model_file):
    f=dll.word_segment_init
    f.argtypes=[c_char_p]
    f.restype=c_uint

    pModel = c_char_p()
    pModel.value = model_file
    print f(pModel)


def Word_segment_for_string(dll, data_in):
    f=dll.word_segment_for_string
    f.argtypes=[c_char_p]

    pData_in = c_char_p()
    pData_in = data_in
    pData_out = create_string_buffer('/0'*1024)
    f(pData_in, pData_out)
    # print pData_out.value.decode("utf-8")
    return pData_out.value


def Word_segment_uninit(dll):
    f=dll.word_segment_uninit
    f.restype=c_uint
    print f()

