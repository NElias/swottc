import random
import math
import logging


def sigmoid(value):
    return 1.0 / (1.0 + math.exp( -float(value) ))


class Kohonen(object):
    def __init__(self, ins=0, hidden=0, outs=0):
        self.whi = []
        self.woh = []
        if ins == hidden == outs == 0:
            return
        for w in xrange(hidden):
            self.whi.append([random.random() * 2 - 1 for i in xrange(ins)])
        for w in xrange(outs):
            ws = [random.random() * 2 - 1 for i in xrange(hidden)]
            self.woh.append(ws)

    def signal(self, *pulses):
        hlayer = []
        for ws in self.whi:
            sum = 0
            for i, w in enumerate(ws):
                sum += pulses[i] * w
            hlayer.append(sigmoid(sum))

        answers = []
        for ws in self.woh:
            sum = 0
            for i, w in enumerate(ws):
                sum += hlayer[i] * w
            answers.append(sigmoid(sum))

        k = None
        m = None
        for i, w in enumerate(answers):
            if m < w:
                m = w
                k = i
        return k

    def signal_eye(self, eye):
        return self.signal(eye.front.predators,
                           eye.front.herbivores,
                           eye.front.plants,

                           eye.left.predators,
                           eye.left.herbivores,
                           eye.left.plants,

                           eye.right.predators,
                           eye.right.herbivores,
                           eye.right.plants,

                           eye.action.predators,
                           eye.action.herbivores,
                           eye.action.plants)

    def copy(self):
        obj = Kohonen()
        obj.whi = list(self.whi)
        obj.woh = list(self.woh)
        return obj

    def mutate(self, n=1):
        for i in xrange(n):
            wch = self.whi if random.randint(0, 1) else self.woh
            n = random.randint(0, len(wch) - 1)
            wch = wch[n]
            n = random.randint(0, len(wch) - 1)
            wch[n] = random.random() * 2 - 1
        return self

    @staticmethod
    def generate(child, one, two):
        for i, ws in enumerate(child.whi):
            child.whi[i] = one.whi[i] if random.randint(0, 1) else two.whi[i]
        for i, ws in enumerate(child.woh):
            child.woh[i] = one.woh[i] if random.randint(0, 1) else two.woh[i]
        return child
