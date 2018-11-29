from pyknow import *
# Run this once
prediction = 10.0 # For testing
input_dict = {} #Create a empty dict - Run Once
exsisting_wt_id = [] # Create an empty list to store the Windturbine ID's - Run Once
cnt = False

RECEIVED_DATA = {'wind_turbine_2': {'status': 'active',
                                    'time': '2010-01-01 00:00:00+01:00',
                                    'output_power': 20.0,
                                    'wind_speed': 5.326969999999998,
                                    'temperature': 267.6,
                                    'pressure': 98405.7}}



def counting_function(RECEIVED_DATA,input_dict,cnt,prediction):
    wind_turbine_id = ''        
    
    # Getting the key from the data received.
    for key in RECEIVED_DATA.keys():
        wind_turbine_id = key
    
    init_ID = [int(s) for s in wind_turbine_id.split('_') if s.isdigit()]
    ID_index = int(init_ID[0])
    
    # Checking if there already is an dict of this ID, if there is,
    # Updating output_power, prediction and status.
    if wind_turbine_id in exsisting_wt_id:
        if cnt == True:
            input_dict[ID_index]['output_power'] = RECEIVED_DATA[wind_turbine_id]['output_power']
            input_dict[ID_index]['prediction']  = prediction
            input_dict[ID_index]['status'] = RECEIVED_DATA[wind_turbine_id]['status']
            input_dict[ID_index]['counter'] = input_dict[ID_index]['counter'] + 1
            cnt = False
            return input_dict
        
        elif cnt == False:
            input_dict[ID_index]['output_power'] = RECEIVED_DATA[wind_turbine_id]['output_power']
            input_dict[ID_index]['prediction']  = prediction
            input_dict[ID_index]['status'] = RECEIVED_DATA[wind_turbine_id]['status']
            input_dict[ID_index]['counter'] = 0
            return input_dict
        
    elif wind_turbine_id not in exsisting_wt_id:
        exsisting_wt_id.append(wind_turbine_id)
        input_dict[ID_index] = {'output_power': RECEIVED_DATA[wind_turbine_id]['output_power'],
                               'prediction': prediction,
                               'status' : RECEIVED_DATA[wind_turbine_id]['status'],
                               'counter' : 0}
        return input_dict

# TODO: Tune margins when power_output increase.

inputs = counting_function(RECEIVED_DATA,input_dict,cnt,prediction)

for key in inputs.keys():
    wt_id = key
#This is the input for the rules
input_data = {'WT_id' : wt_id,
              'output_power' : inputs[wt_id]['output_power'],
              'prediction' : inputs[wt_id]['prediction'],
              'status' : inputs[wt_id]['status'],
              'counter' : inputs[wt_id]['counter']
             }


output_status = {'WT_id' : 0,  'status_out' : '', 'counter' : False}


class Input(Fact):
    pass

class Output(Fact):
    def retrieve(self):
        return self.as_dict()

class State(Fact):
    pass

class Detection(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.returnv={}

    # Rule for detecting abnormal power production
    @Rule(Input(output_power=MATCH.out_p,
                prediction=MATCH.pred,
                WT_id=MATCH.ID,
                counter=MATCH.c),
          TEST(lambda out_p, pred, c: ( c <= 2) and ((out_p >= 1.20*pred) or (out_p <= 0.80*pred))),
          salience=5)
    def bad_state1(self):
        self.declare(State(P_prod = True))
        self.declare(Output(counter=True))
        print("Abnormal production!")
        
    # Rule for detecting broken wind turbine
    @Rule(Input(output_power=MATCH.out_p,
                prediction=MATCH.pred,
                WT_id=MATCH.ID,
                counter=MATCH.c),
          TEST(lambda out_p, pred, c: ( c > 2) and ((out_p >= 1.20*pred) or (out_p <= 0.80*pred))),
          salience=5)
    def bad_state2(self):
        self.declare(State(P_prod = False))
        self.declare(Output(counter=True))
        
    # Rule for detecting normal power production
    @Rule(Input(output_power=MATCH.out_p,
                prediction=MATCH.pred,
                WT_id=MATCH.ID),
          TEST(lambda out_p, pred: (out_p <= 1.20*pred) and (out_p >= 0.80*pred)),
          salience=5)
    def good_state(self):
        self.declare(State(P_prod = True))
        print("Normal production!")

    # Rule for checking if wind turbine has been shut down for repair.   
    @Rule(AS.f << Input(output_power=MATCH.out_p,
                  WT_id=MATCH.ID,
                  status="inactive"),
          TEST(lambda out_p: out_p == 0.0),
          salience=5)
    def wt_repair(self,ID,f):
        self.retract(f)
        self.declare(Output(WT_id = ID, status_out="inactive"))
        print("Wind turbine "+str(ID)+" has been shut down for repair.")

    # Rule for changing state of the wind turbine to inactive.
    @Rule(Input(WT_id=MATCH.ID),
          State(P_prod=False),
          salience=3)
    def change_state1(self,ID):
        self.declare(Output(WT_id = ID, status_out="inactive"))
        print("Wind turbine "+str(ID)+" is inactive.")

    # Rule for changing state of the wind turbine to active.
    @Rule(Input(WT_id=MATCH.ID),
          State(P_prod=True),
          salience=3)
    def change_state2(self,ID):
        self.declare(Output(WT_id = ID, status_out="active" ))
        print("Wind turbine "+str(ID)+" is active.")

    @Rule(AS.out << Output(),              
          salience=0)
    def _returnstate(self,out):
        self.returnv.update(**out.retrieve())
        #print("Status for Wind Turbine: " +str(out.retrieve()))

    def get_return(self,key):
        return self.returnv.get(key)



wt = Detection()
wt.reset()
wt.declare(Input(**input_data)) 
wt.returnv={}
wt.run()


output_status.update([(key, wt.returnv[key]) for key in wt.returnv.keys()])
Wind_turbine_status = output_status

cnt = Wind_turbine_status['counter']
print(Wind_turbine_status)
print(input_data)


