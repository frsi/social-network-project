from abc import ABCMeta, abstractmethod
from random import randint



# Bots:
#   INPUT
#       - Name (?)
#       - Personal Evaluation
#       - Bid History
#         |- Bids       KEY: Advertisers    VALUE: Bids
#         |- Slots      KEY: Advertisers    VALUE: Slots
#         '- Pays       KEY: Advertisers    VALUE: Prices
#       - Slots Clickthrough Rates
#       - Current Budget
#       - Initial Budget
#   OUTPUT
#       - Bid




class Bot(metaclass=ABCMeta):
    @abstractmethod
    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):
        pass


def evaluate_slots(sorted_slots_clicktr, sorted_last_step_bids, slot_ctrs, last_slot, evaluation):
    utility = -1
    preferred_slot = -1
    payment = 0

    #The best response bot makes the following steps:
    #1) Evaluate for each slot, how much the advertiser would pay if
    #   - he changes his bid so that that slot is assigned to him
    #   - no other advertiser change the bid
    for i in range(len(sorted_slots_clicktr)):

        if i < last_slot: #If I take a slot better than the one previously assigned to me
            tmp_pay = sorted_last_step_bids[i] #then, I must pay for that slot the bid of the advertiser at which that slot was previously assigned
        elif i == len(sorted_last_step_bids) - 1: #If I take the last slot, I must pay 0
            tmp_pay = 0
        else:    #If I take the slot as before or a worse one (but not the last)
            tmp_pay = sorted_last_step_bids[i+1]

        #2) Evaluate for each slot, which one gives to the advertiser the largest utility
        new_utility = slot_ctrs[sorted_slots_clicktr[i]]*(evaluation - tmp_pay)

        if new_utility > utility :
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay
    return utility, preferred_slot, payment

class Bot1(Bot):
    """Best-response bot with balanced tie-breaking rule"""
    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):
        step = len(history)

        #If this is the first step there is no history and no best-response is possible
        #We suppose that adevertisers simply bid their value.
        #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
        if step == 0:
            return 0

        #Initialization
        last_step_slots = history[step-1]["adv_slots"]
        last_step_bids = history[step-1]["adv_bids"]

        sorted_last_step_bids = sorted(last_step_bids.values(), reverse = True)
        sorted_slots_clicktr = sorted(slot_ctrs.keys(), key = slot_ctrs.__getitem__, reverse = True)

        #Saving the index of slots assigned at the advertiser in the previous auction
        if name not in last_step_slots.keys():
            last_slot = -1
        else:
            last_slot = sorted_slots_clicktr.index(last_step_bids[name])

        utility, preferred_slot, payment = evaluate_slots(sorted_slots_clicktr, sorted_last_step_bids, slot_ctrs, last_slot, evaluation)

        #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
        if preferred_slot == -1:
            # TIE-BREAKING RULE: I choose the largest bid smaller than my value for which I lose
            return min(evaluation, sorted_last_step_bids)

        if preferred_slot == 0:
            # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
            return float(evaluation+payment)/2

        #TIE-BREAKING RULE: If I like slot j, I choose the bid b_i for which I am indifferent from taking j at computed price or taking j-1 at price b_i
        return (evaluation - float(slot_ctrs[sorted_last_step_bids[preferred_slot]])/slot_ctrs[sorted_last_step_bids[preferred_slot-1]] * (evaluation - payment))


class Bot2(Bot):
    """Best-response bot with competitor bursting tie-breaking rule"""
    """Submit the highest possible bid that gives the desired slot"""
    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):
        step = len(history)

        #If this is the first step there is no history and no best-response is possible
        #We suppose that adevertisers simply bid their value.
        #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
        if step == 0:
            return 0

        #Initialization
        last_step_slots = history[step-1]["adv_slots"]
        last_step_bids = history[step-1]["adv_bids"]

        sorted_last_step_bids = sorted(last_step_bids.values(), reverse = True)
        sorted_slots_clicktr = sorted(slot_ctrs.keys(), key = slot_ctrs.__getitem__, reverse = True)

        #Saving the index of slots assigned at the advertiser in the previous auction
        if name not in last_step_slots.keys():
            last_slot = -1
        else:
            last_slot = sorted_slots_clicktr.index(last_step_bids[name])

        utility, preferred_slot, payment = evaluate_slots(sorted_slots_clicktr, sorted_last_step_bids, slot_ctrs, last_slot, evaluation)

        #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
        if preferred_slot == -1:
            # TIE-BREAKING RULE: I choose the largest bid smaller than my value for which I lose
            return min(evaluation, sorted_last_step_bids)

        if preferred_slot == 0:
            # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
            return float(evaluation+payment)/2

        

        #TIE-BREAKING RULE: Submit the highest possible bid that gives the desired slot
        return sorted_last_step_bids[preferred_slot-1] - 1





class Bot3(Bot):
    """Best-response bot with altruistic bidding tie-breaking rule"""
    """Submit the lowest possible bid that gives the desired slot"""
    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):
        step = len(history)

        #If this is the first step there is no history and no best-response is possible
        #We suppose that adevertisers simply bid their value.
        #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
        if step == 0:
            return 0

        #Initialization
        last_step_slots = history[step-1]["adv_slots"]
        last_step_bids = history[step-1]["adv_bids"]

        sorted_last_step_bids = sorted(last_step_bids.values(), reverse = True)
        sorted_slots_clicktr = sorted(slot_ctrs.keys(), key = slot_ctrs.__getitem__, reverse = True)

        #Saving the index of slots assigned at the advertiser in the previous auction
        if name not in last_step_slots.keys():
            last_slot = -1
        else:
            last_slot = sorted_slots_clicktr.index(last_step_bids[name])

        utility, preferred_slot, payment = evaluate_slots(sorted_slots_clicktr, sorted_last_step_bids, slot_ctrs, last_slot, evaluation)

        #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
        if preferred_slot == -1:
            # TIE-BREAKING RULE: I choose the largest bid smaller than my value for which I lose
            return min(evaluation, sorted_last_step_bids)

        if preferred_slot == 0:
            # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
            return float(evaluation+payment)/2

        #TIE-BREAKING RULE: Submit the lowest possible bid that gives the desired slot
        return sorted_last_step_bids[preferred_slot]

class Bot4(Bot):
    """Competitor-bursting bot"""
    """Submit the highest bid seen in previous auctions, even if it is greater than own value"""
    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):

        step = len(history)

        if step == 0:
            return 0

        last_step_bids = history[step-1]["adv_bids"]
        return max(last_step_bids)

class Bot5(Bot):
    """Budget-saving bot"""
    """Submit minimum among the last non-winning bid and the advertiser value for the query"""
    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):

        step = len(history)

        if step == 0:
            return 0

        last_step_bids = history[step-1]["adv_bids"]
        min_bid_last_step = min(last_step_bids)

        return min(min_bid_last_step, evaluation)

class Bot6(Bot):
    """Random bot"""
    """Submit random bid"""
    def response(self,name,bids,slot_ctrs,history):

        step = len(history)

        if step == 0:
            return 0

        last_step_bids = history[step-1]["adv_bids"]
        min_bid_last_step = min(last_step_bids)
        max_bid_last_step = max(last_step_bids)

        return randint(min_bid_last_step,max_bid_last_step)

class Bot7(Bot):
    """Combination of the above bots based on the current badget or the advertiser value for the current query"""
    
    def response(self,name,bids,slot_ctrs,history):
        return

#We implement a possible bot for an advertiser in a repeated GSP auction
#The bot of an advertiser is a program that, given the history of what occurred in previous auctions, suggest a bid for the next auction.
#Specifically, a bot takes in input
#- the name of the advertiser (it allows to use the same bot for multiple advertisers)
#- the value of the advertiser (it is necessary for evaluating the utility of the advertiser)
#- the clickthrough rates of the slots
#- the history
#We assume the history is represented as an array that contains an entry for each time step,
#i.e. history[i] contains the information about the i-th auction.
#In particular, for each time step we have that 
#- history[i]["adv_bids"] returns the advertisers' bids as a dictionary in which the keys are advertisers' names and values are their bids
#- history[i]["adv_slots"] returns the assignment as a dictionary in which the keys are advertisers' names and values are their assigned slots
#- history[i]["adv_pays"] returns the payments as a dictionary in which the keys are advertisers' names and values are their assigned prices

#The bot that we implement here is a symple best_response bot:
#it completely disregards the history except the last step,
#and suggest the bid that will maximize the advertiser utility
#given that the other advertisers do not change their bids.
def best_response(name, adv_value, slot_ctrs, history):
    
    step = len(history)
    
    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    if step == 0:
        return 0
    
    #Initialization
    adv_slots=history[step-1]["adv_slots"]
    adv_bids=history[step-1]["adv_bids"]
    
    sort_bids=sorted(adv_bids.values(), reverse=True)
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    
    #Saving the index of slots assigned at the advertiser in the previous auction
    if name not in adv_slots.keys():
        last_slot=-1
    else:
        last_slot=sort_slots.index(adv_slots[name])
        
    utility = -1
    preferred_slot = -1
    payment = 0

    #The best response bot makes the following steps:
    #1) Evaluate for each slot, how much the advertiser would pay if
    #   - he changes his bid so that that slot is assigned to him
    #   - no other advertiser change the bid
    for i in range(len(sort_slots)):
        
        if i < last_slot: #If I take a slot better than the one previously assigned to me
            tmp_pay = sort_bids[i] #then, I must pay for that slot the bid of the advertiser at which that slot was previously assigned
            
        elif i == len(sort_bids) - 1: #If I take the last slot, I must pay 0
            tmp_pay = 0
            
        else: #If I take the slot as before or a worse one (but not the last)
            tmp_pay = sort_bids[i+1] #then, I must pay for that slot the bid of the next advertiser
        
    #2) Evaluate for each slot, which one gives to the advertiser the largest utility
        new_utility = slot_ctrs[sort_slots[i]]*(adv_value-tmp_pay)
        
        if new_utility > utility:
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay
    
    #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
    if preferred_slot == -1:
        # TIE-BREAKING RULE: I choose the largest bid smaller than my value for which I lose
        return min(adv_value, sort_bids[len(sort_slots)])
    
    if preferred_slot == 0:
        # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
        return float(adv_value+payment)/2
    
    #TIE-BREAKING RULE: If I like slot j, I choose the bid b_i for which I am indifferent from taking j at computed price or taking j-1 at price b_i
    return (adv_value - float(slot_ctrs[sort_slots[preferred_slot]])/slot_ctrs[sort_slots[preferred_slot-1]] * (adv_value - payment))














