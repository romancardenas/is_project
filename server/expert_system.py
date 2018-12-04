from pyknow import *


class Counter(Fact):
    pass


class Result(Fact):
    pass


class Input(Fact):
    pass


class Output(Fact):
    def retrieve(self):
        return self.as_dict()


class State(Fact):
    pass


class ExpertSystem(KnowledgeEngine):
    def __init__(self, n_count):
        super().__init__()
        self.returnv = dict()
        self.cnt = dict()
        self.N_COUNTS = n_count
        self.reset()

    def evaluate(self, idn, data, prediction):
        i = 0
        if idn not in list(self.cnt.keys()):
            i = 1
            self.cnt[idn] = 0
        input_data = data.copy()
        input_data['WT_id'] = idn  # we add to data the ID
        input_data['prediction'] = prediction  # we add to data the prediction

        counter_data = dict()
        counter_data['WT_id'] = idn  # we add to data the ID
        counter_data['counter'] = self.cnt[idn]  # we add to data the counter
        counter_data['maxim'] = self.N_COUNTS  # we add to data the counter
        if i:
            self.declare(Counter(**counter_data))
        self.declare(Input(**input_data))
        self.returnv = dict()
        self.run()
        self.cnt[idn] = self.returnv['counter']
        return self.returnv['response']

    # Folling rules sets the upper and lower limits, depening on what the power output is.
    @Rule(Input(status='active',
                WT_id=MATCH.ID,
                output_power=MATCH.out_p),
          TEST(lambda out_p: out_p <= 2500000),
          salience=7)
    def set_limit1(self, ID):
        self.declare(State(WT_id=ID, flag="L_1"))

    @Rule(Input(status='active',
                WT_id=MATCH.ID,
                output_power=MATCH.out_p),
          TEST(lambda out_p: (2800000 >= out_p > 2500000)),
          salience=7)
    def set_limit2(self, ID):
        self.declare(State(WT_id=ID, flag="L_2"))

    @Rule(Input(status='active',
                WT_id=MATCH.ID,
                output_power=MATCH.out_p),
          TEST(lambda out_p: (5000000 >= out_p > 2800000)),
          salience=7)
    def set_limit3(self, ID):
        self.declare(State(WT_id=ID, flag="L_3"))

    @Rule(Input(status='active',
                WT_id=MATCH.ID,
                output_power=MATCH.out_p),
          TEST(lambda out_p: (5600000 >= out_p > 5000000)),
          salience=7)
    def set_limit4(self, ID):
        self.declare(State(WT_id=ID, flag="L_4"))

    @Rule(Input(status='active',
                WT_id=MATCH.ID,
                output_power=MATCH.out_p),
          TEST(lambda out_p: (8000000 >= out_p > 5600000)),
          salience=7)
    def set_limit5(self, ID):
        self.declare(State(WT_id=ID, flag="L_5"))
     
    @Rule(Input(status='active',
                WT_id=MATCH.ID,
                output_power=MATCH.out_p),
          TEST(lambda out_p: (out_p > 8000000)),
          salience=7)
    def set_limit6(self, ID):
        self.declare(State(WT_id=ID, flag="L_6"))

    @Rule(AS.i << Input(output_power=MATCH.out_p,
                        prediction=MATCH.pred,
                        WT_id=MATCH.ID,
                        status='active'),
          AS.f << Counter(WT_id=MATCH.ID,
                          counter=MATCH.c),
          AS.s << State(WT_id=MATCH.ID,
                        flag="L_1"),
          TEST(lambda out_p, pred: (out_p >= 1.2 * (pred + 2e5)) or (out_p < 0.8 * (pred - 2e5))),
          salience=5)
    def bad_state_1(self, c, f, i, s, ID):
        print("Abnormal production1! {}".format(c+1))
        c += 1
        self.modify(f, counter=c)
        self.retract(i)
        self.retract(s)
        self.declare(Result(WT_id=ID))

    # Rule for detecting abnormal power production
    @Rule(AS.i << Input(output_power=MATCH.out_p,
                        prediction=MATCH.pred,
                        WT_id=MATCH.ID,
                        status='active'),
          AS.f << Counter(WT_id=MATCH.ID,
                          counter=MATCH.c),
          AS.s << State(WT_id=MATCH.ID,
                        flag="L_2"),
          TEST(lambda out_p, pred: (out_p >= (1.1 * (pred + 2e5)+0.2e6)) or (out_p < 0.8 * (pred - 2e5))),
          salience=5)
    def bad_state_2(self, c, f, i, s, ID):
        print("Abnormal production2 {}".format(c+1))
        c += 1
        self.modify(f, counter=c)
        self.retract(i)
        self.retract(s)
        self.declare(Result(WT_id=ID))

        # Rule for detecting abnormal power production

    @Rule(AS.i << Input(output_power=MATCH.out_p,
                        prediction=MATCH.pred,
                        WT_id=MATCH.ID,
                        status='active'),
          AS.f << Counter(WT_id=MATCH.ID,
                          counter=MATCH.c),
          AS.s << State(WT_id=MATCH.ID,
                        flag="L_3"),
          TEST(lambda out_p, pred: (out_p >= (1.1 * (pred + 2e5)+0.2e6)) or (out_p < (1.12 * (pred - 2e5)-0.9e6))),
          salience=5)
    def bad_state_3(self, c, f, i, s, ID):
        print("Abnormal production3! {}".format(c+1))
        c += 1
        self.modify(f, counter=c)
        self.retract(i)
        self.retract(s)
        self.declare(Result(WT_id=ID))

        # Rule for detecting abnormal power production

    @Rule(AS.i << Input(output_power=MATCH.out_p,
                        prediction=MATCH.pred,
                        WT_id=MATCH.ID,
                        status='active'),
          AS.f << Counter(WT_id=MATCH.ID,
                          counter=MATCH.c),
          AS.s << State(WT_id=MATCH.ID,
                        flag="L_4"),
          TEST(lambda out_p, pred: (out_p >= (0.76 * (pred + 2e5)+1.8e6)) or (out_p < (1.12*(pred - 2e5)-0.9e6))),
          salience=5)
    def bad_state_4(self, c, f, i, s, ID):
        print("Abnormal production4! {}".format(c+1))
        c += 1
        self.modify(f, counter=c)
        self.retract(i)
        self.retract(s)
        self.declare(Result(WT_id=ID))

    @Rule(AS.i << Input(output_power=MATCH.out_p,
                        prediction=MATCH.pred,
                        WT_id=MATCH.ID,
                        status='active'),
          AS.f << Counter(WT_id=MATCH.ID,
                          counter=MATCH.c),
          AS.s << State(WT_id=MATCH.ID,
                        flag="L_5"),
          TEST(lambda out_p, pred: (out_p >= (0.65 * (pred + 2e5)+2.5e6)) or (out_p < (1.12 * (pred - 2e5)-0.9e6))),
          salience=5)
    def bad_state_5(self, c, f, i, s, ID):
        print("Abnormal production5! {}".format(c+1))
        c += 1
        self.modify(f, counter=c)
        self.retract(i)
        self.retract(s)
        self.declare(Result(WT_id=ID))
        
    @Rule(AS.i << Input(output_power=MATCH.out_p,
                        prediction=MATCH.pred,
                        WT_id=MATCH.ID,
                        status='active'),
          AS.f << Counter(WT_id=MATCH.ID,
                          counter=MATCH.c),
          AS.s << State(WT_id=MATCH.ID,
                        flag="L_6"),
          TEST(lambda out_p, pred: (out_p >= (out_p < (0.8 * (pred - 2e5)+0.8e6)),
          salience=5)
    def bad_state_6(self, c, f, i, s, ID):
        print("Abnormal production6! {}".format(c+1))
        c += 1
        self.modify(f, counter=c)
        self.retract(i)
        self.retract(s)
        self.declare(Result(WT_id=ID))

    @Rule(AS.i << Input(output_power=MATCH.out_p,
                        prediction=MATCH.pred,
                        WT_id=MATCH.ID,
                        status='active'),
          AS.f << Counter(WT_id=MATCH.ID,
                          counter=MATCH.c),
          AS.s << State(WT_id=MATCH.ID,
                        flag="L_1"),
          TEST(lambda out_p, pred: (1.2 * (pred + 2e5)) > out_p >= (0.8 * (pred - 2e5))),
          salience=5)
    def good_state_1(self, f, i, s, ID, c):
        print("Normal production1! {}".format(c))
        if c > 0:
            c -= 1
        else:
            c = 0
        self.modify(f, counter=c)
        self.retract(i)
        self.retract(s)
        self.declare(Result(WT_id=ID))

    @Rule(AS.i << Input(output_power=MATCH.out_p,
                        prediction=MATCH.pred,
                        WT_id=MATCH.ID,
                        status='active'),
          AS.f << Counter(WT_id=MATCH.ID,
                          counter=MATCH.c),
          AS.s << State(WT_id=MATCH.ID,
                        flag="L_2"),
          TEST(lambda out_p, pred: (1.1 * (pred + 2e5)+0.2e6) > out_p >= (0.8 * (pred - 2e5))),
          salience=5)
    def good_state_2(self, f, i, s, ID, c):
        print("Normal production2! {}".format(c))
        if c > 0:
            c -= 1
        else:
            c = 0
        self.modify(f, counter=c)
        self.retract(i)
        self.retract(s)
        self.declare(Result(WT_id=ID))

    @Rule(AS.i << Input(output_power=MATCH.out_p,
                        prediction=MATCH.pred,
                        WT_id=MATCH.ID,
                        status='active'),
          AS.f << Counter(WT_id=MATCH.ID,
                          counter=MATCH.c),
          AS.s << State(WT_id=MATCH.ID,
                        flag="L_3"),
          TEST(lambda out_p, pred: (1.1 * (pred + 2e5)+0.2e6) > out_p >= (1.12 * (pred - 2e5)-0.9e6)),
          salience=5)
    def good_state_3(self, f, i, s, ID, c):
        print("Normal production3! {}".format(c))
        if c > 0:
            c -= 1
        else:
            c = 0
        self.modify(f, counter=c)
        self.retract(i)
        self.retract(s)
        self.declare(Result(WT_id=ID))

        # Rule for detecting abnormal power production

    @Rule(AS.i << Input(output_power=MATCH.out_p,
                        prediction=MATCH.pred,
                        WT_id=MATCH.ID,
                        status='active'),
          AS.f << Counter(WT_id=MATCH.ID,
                          counter=MATCH.c),
          AS.s << State(WT_id=MATCH.ID,
                        flag="L_4"),
          TEST(lambda out_p, pred: (0.76 * (pred + 2e5)+1.8e6) > out_p >= (1.12*(pred - 2e5)-0.9e6)),
          salience=5)
    def good_state_4(self, f, i, s, ID, c):
        print("Normal production4! {}".format(c))
        if c > 0:
            c -= 1
        else:
            c = 0
        self.modify(f, counter=c)
        self.retract(i)
        self.retract(s)
        self.declare(Result(WT_id=ID))

    @Rule(AS.i << Input(output_power=MATCH.out_p,
                        prediction=MATCH.pred,
                        WT_id=MATCH.ID,
                        status='active'),
          AS.f << Counter(WT_id=MATCH.ID,
                          counter=MATCH.c),
          AS.s << State(WT_id=MATCH.ID,
                        flag="L_5"),
          TEST(lambda out_p, pred: (0.65 * (pred + 2e5)+2.5e6) > out_p >= (1.12 * (pred+2e5)-0.9e6))),
          salience=5)
    def good_state_5(self, f, i, s, ID, c):
        print("Normal production5! {}".format(c))
        if c > 0:
            c -= 1
        else:
            c = 0
        self.modify(f, counter=c)
        self.retract(i)
        self.retract(s)
        self.declare(Result(WT_id=ID))

    @Rule(AS.i << Input(output_power=MATCH.out_p,
                        prediction=MATCH.pred,
                        WT_id=MATCH.ID,
                        status='active'),
          AS.f << Counter(WT_id=MATCH.ID,
                          counter=MATCH.c),
          AS.s << State(WT_id=MATCH.ID,
                        flag="L_6"),
          TEST(lambda out_p, pred: (0.8 * (pred + 2e5)+0.8e6) > out_p),
          salience=5)
    def good_state_6(self, f, i, s, ID, c):
        print("Normal production6! {}".format(c))
        if c > 0:
            c -= 1
        else:
            c = 0
        self.modify(f, counter=c)
        self.retract(i)
        self.retract(s)
        self.declare(Result(WT_id=ID))
          
          
    @Rule(AS.i << Input(WT_id=MATCH.ID,
                        status='stop'),
          AS.f << Counter(WT_id=MATCH.ID,
                          counter=MATCH.c),
          salience=2)
    def reset_counter(self, f, ID, i, c):

        self.modify(f, counter=0)
        self.retract(i)
        self.declare(Output(id=ID, response="stop", counter=0))

    # If we exceed the counter -> return stop
    @Rule(AS.r << Result(WT_id=MATCH.ID),
          AS.f << Counter(WT_id=MATCH.ID,
                          counter=MATCH.c,
                          maxim=MATCH.m),
          TEST(lambda c, m: c >= m),
          salience=2)
    def stop_turbine(self, ID, f, r, c):
        self.modify(f, counter=0)
        self.retract(r)
        self.declare(Output(id=ID, response="stop", counter=c))

    # If we don't exceed the counter -> return active
    @Rule(AS.r << Result(WT_id=MATCH.ID),
          AS.f << Counter(WT_id=MATCH.ID,
                          counter=MATCH.c,
                          maxim=MATCH.m),
          TEST(lambda c, m: c < m),
          salience=2)
    def start_turbine(self, ID, r, c):
        self.retract(r)
        self.declare(Output(id=ID, response="active", counter=c))

    @Rule(AS.out << Output(), salience=0)
    def _returnstate(self, out):
        self.returnv.update(**out.retrieve())
        self.retract(out)

    def get_return(self, key):
        return self.returnv.get(key)
