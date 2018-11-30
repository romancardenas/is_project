from pyknow import *

N_COUNTS = 10
# TODO change this


class Input(Fact):
    pass


class Output(Fact):
    def retrieve(self):
        return self.as_dict()


class State(Fact):
    pass


class Detection(KnowledgeEngine):

    def __init__(self, n_count):
        super().__init__()
        self.returnv={}
        N_COUNTS = n_count

    # Folling rules sets the upper and lower limits, depening on what the power output is.
    @Rule(Input(output_power=MATCH.out_p),
          TEST(lambda out_p: out_p <= 2300000),
          salience=7)
    def set_limit1(self):
        self.declare(State(flag="L_1"))
            
    @Rule(Input(output_power=MATCH.out_p),
          TEST(lambda out_p: (4000000 >= out_p > 2300000)),
          salience=7)
    def set_limit2(self):
        self.declare(State(flag="L_2"))
            
    @Rule(Input(output_power=MATCH.out_p),
          TEST(lambda out_p: (5600000 >= out_p > 4000000)),
          salience=7)
    def set_limit3(self):
        self.declare(State(flag="L_3"))
         
    @Rule(Input(output_power=MATCH.out_p),
          TEST(lambda out_p: (7000000 >= out_p > 5600000)),
          salience=7)
    def set_limit4(self):
        self.declare(State(flag="L_4"))

            
    @Rule(Input(output_power=MATCH.out_p),
          TEST(lambda out_p: (out_p > 7000000)),
          salience=7)
    def set_limit5(self):
        self.declare(State(flag="L_5"))

        # Rule for detecting abnormal power production
    @Rule(Input(output_power=MATCH.out_p,
                prediction=MATCH.pred,
                WT_id=MATCH.ID,
                counter=MATCH.c),
          State(flag="L_1"),
          TEST(lambda out_p, pred, c: ( c <= N_COUNTS) and ((out_p >= 1.20*pred) or (out_p <= 0.8*pred))),
          salience=5)
    def bad_state_1(self):
        self.declare(State(P_prod = True))
        self.declare(Output(counter=True))
        print("Abnormal production1!")
            
        # Rule for detecting abnormal power production
    @Rule(Input(output_power=MATCH.out_p,
                prediction=MATCH.pred,
                WT_id=MATCH.ID,
                counter=MATCH.c),
          State(flag="L_2"),
          TEST(lambda out_p, pred, c: ( c <= N_COUNTS) and ((out_p >= 1.2*pred) or (out_p <= 0.85*pred))),
          salience=5)
    def bad_state_2(self):
        self.declare(State(P_prod = True))
        self.declare(Output(counter=True))
        print("Abnormal production2!")
            
        # Rule for detecting abnormal power production
    @Rule(Input(output_power=MATCH.out_p,
                prediction=MATCH.pred,
                WT_id=MATCH.ID,
                counter=MATCH.c),
          State(flag="L_3"),
          TEST(lambda out_p, pred, c: ( c <= N_COUNTS) and ((out_p >= 1.1*pred) or (out_p <= 0.85*pred))),
          salience=5)
    def bad_state_3(self):
        self.declare(State(P_prod = True))
        self.declare(Output(counter=True))
        print("Abnormal production3!")
            
        # Rule for detecting abnormal power production
    @Rule(Input(output_power=MATCH.out_p,
                prediction=MATCH.pred,
                WT_id=MATCH.ID,
                counter=MATCH.c),
          State(flag="L_4"),
          TEST(lambda out_p, pred, c: ( c <= N_COUNTS) and (out_p >= 1.1*pred)), 
          salience=5)
    def bad_state_4(self):
        self.declare(State(P_prod = True))
        self.declare(Output(counter=True))
        print("Abnormal production4!")
            
    @Rule(Input(output_power=MATCH.out_p,
                prediction=MATCH.pred,
                WT_id=MATCH.ID,
                counter=MATCH.c),
          State(flag="L_5"),
          TEST(lambda out_p, pred, c: ( c <= N_COUNTS) and (out_p >= 1.15*pred)), #lower lim?
          salience=5)
    def bad_state_5(self):
        self.declare(State(P_prod = True))
        self.declare(Output(counter=True))
        print("Abnormal production5!") 
        
    # Rule for detecting broken wind turbine
    @Rule(Input(output_power=MATCH.out_p,
                prediction=MATCH.pred,
                WT_id=MATCH.ID,
                counter=MATCH.c),
          TEST(lambda out_p, pred, c: ( c > N_COUNTS) and ((out_p >= 1.20*pred) or (out_p <= 0.80*pred))),
          salience=5)
    def bad_state2(self):
        self.declare(State(P_prod = False))
        self.declare(Output(counter=True))
        
        # Rule for detecting normal power production
    @Rule(Input(output_power=MATCH.out_p,
                prediction=MATCH.pred,
                WT_id=MATCH.ID),
          State(flag="L_1"),
          TEST(lambda out_p, pred: (out_p <= 1.20*pred) and (out_p >= 0.80*pred)),
          salience=5)
    def good_state_1(self):
        self.declare(State(P_prod = True))
        print("Normal production1!")
            
    @Rule(Input(output_power=MATCH.out_p,
                prediction=MATCH.pred,
                WT_id=MATCH.ID),
          State(flag="L_2"),
          TEST(lambda out_p, pred: (out_p <= 1.20*pred) and (out_p >= 0.85*pred)),
          salience=5)
    def good_state_2(self):
        self.declare(State(P_prod = True))
        print("Normal production2!")
        
    @Rule(Input(output_power=MATCH.out_p,
                prediction=MATCH.pred,
                WT_id=MATCH.ID),
          State(flag="L_3"),
          TEST(lambda out_p, pred: (out_p <= 1.1*pred) and (out_p >= 0.85*pred)),
          salience=5)
    def good_state_3(self):
        self.declare(State(P_prod = True))
        print("Normal production3!")
            
    @Rule(Input(output_power=MATCH.out_p,
                prediction=MATCH.pred,
                WT_id=MATCH.ID),
          State(flag="L_4"),
          TEST(lambda out_p, pred: (out_p <= 1.1*pred)),
          salience=5)
    def good_state_4(self):
        self.declare(State(P_prod = True))
        print("Normal production4!")
            
    @Rule(Input(output_power=MATCH.out_p,
                prediction=MATCH.pred,
                WT_id=MATCH.ID),
          State(flag="L_5"),
          TEST(lambda out_p, pred: (out_p <= 1.15*pred)),
          salience=5)
    def good_state_5(self):
        self.declare(State(P_prod = True))
        print("Normal production5!")

    # Rule for checking if wind turbine has been shut down for repair.   
    @Rule(AS.f << Input(output_power=MATCH.out_p,
                  WT_id=MATCH.ID,
                  status="stop"),
          TEST(lambda out_p: out_p == 0.0),
          salience=5)
    def wt_repair(self,ID,f):
        self.retract(f)
        self.declare(Output(WT_id = ID, status_out="stop"))
        print("Wind turbine "+str(ID)+" has been shut down for repair.")

    # Rule for changing state of the wind turbine to inactive.
    @Rule(Input(WT_id=MATCH.ID),
          State(P_prod=False),
          salience=3)
    def change_state1(self,ID):
        self.declare(Output(WT_id = ID, status_out="stop"))
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
