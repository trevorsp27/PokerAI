##poker player strategy and i/o

import random, pokerhands
from collections import Counter
import math

def evaluate(player):
	
	value=player.get_value()
	
def calc_bet(player):

                   
        max_bet=player.stack-player.to_play
        min_bet=player.to_play
        if max_bet<min_bet:
        	min_bet=max_bet
        print ('max bet '+str(max_bet))
        print ('min be  '+str(min_bet))
        
        

        if max_bet<0:
                max_bet=player.stack
				
        bet_amount=random.randrange(min_bet,max_bet+1,5)
        
        
        return bet_amount
	

class Strategy():
        
        def __init__(self, player):
                
                self.tight=0
                self.aggression=0
                self.cool=0
                self.player=player
                self.name=str(self.__class__.__name__)

        
              
        @property
        
        def play_style(self):
                
                pass

        def decide_play(self, player, pot):
                
                pass


class ScoreBet(Strategy):

        def decide_play(self, player, pot):

                total_blinds = (pot.blinds[0] + pot.blinds[1])
                score = (player.stack / total_blinds)
                score *= pot.yet_to_play
                score *= (pot.limpers + 1)
                score = int(score)

                hand_value, rep, tie_break, raw_data = player.get_value()
                raw_values, flush_score, straight, gappers = raw_data
                raw_values.sort()

                key = (
                (range(0, 19)), (range(20, 39)), (range(40, 59)), (range(60, 79)), (range(80, 99)), (range(100, 149)),
                (range(150, 199)), (range(200, 399)), (range(400, 1000)))

                for k in key:
                        if score in k:
                                pointer = key.index(k)

                toBet = False

                print('score=' + str(score))
                print('pot raised=' + str(pot.raised))

                if pot.raised:

                        if raw_values in ((13, 13), (12, 12)):
                                toBet = True

                        elif raw_values in (13, 12) and flush_score == 2:
                                toBet = True

                        else:
                                toBet = False

                elif score > 400 and raw_values in (13, 13):
                        toBet = True
                elif score in range(200, 399) and raw_values in ((13, 13), (12, 12)):
                        toBet = True
                elif score in range(150, 199) and raw_values in ((13, 13), (12, 12), (11, 11), (13, 12)):
                        toBet = True
                elif score in range(100, 149) and raw_values in (
                (13, 13), (12, 12), (11, 11), (10, 10), (9, 9), (13, 12), (13, 11), (12, 11)):
                        toBet = True
                elif score in range(80, 99):
                        if 'pair' in rep:
                                toBet = True
                        elif raw_values in ((13, 12), (13, 11), (12, 11)):
                                toBet = True
                        elif flush_score == 2 and 13 in raw_values:
                                toBet = True
                        elif flush_score == 2 and straight >= 5:
                                toBet = True
                elif score in range(60, 79):
                        if 'pair' in rep:
                                toBet = True
                        elif 13 in raw_values:
                                toBet = True
                        elif flush_score == 2 and 12 in raw_values:
                                toBet = True
                        elif flush_score == 2 and gappers <= 1:
                                toBet = True
                elif score in range(40, 59):
                        if 'pair' in rep:
                                toBet = True
                        elif 13 or 12 in raw_values:
                                toBet = True
                        elif flush_score == 2 and 12 in raw_values:
                                toBet = True
                        elif flush_score == 2 and gappers <= 1:
                                toBet = True
                elif score in range(20, 39):
                        if 'pair' in rep:
                                toBet = True
                        elif 13 or 12 in raw_values:
                                toBet = True
                        elif flush_score == 2:
                                toBet = True
                else:
                        toBet = False

                if toBet:
                        if player.stack <= player.to_play:
                                if not pot.raised:
                                        player.bet(pot, score)
                                else:
                                        player.check_call(pot)
                        elif not pot.raised:
                                player.bet(pot, player.stack)
                else:
                        player.fold(pot)

			
class RiskReward(Strategy):

        def decide_play(self, player, pot):
                self.aggression = 1
                self.tight = 1

                hand_value, rep, tie_break, raw_data = player.get_value()
                raw_values, flush_score, straight, gappers = raw_data
                raw_values.sort()
                print(raw_values)
                print(straight)


                probBetterHand = self.prob_better_hand(player, hand_value)
                if probBetterHand == 0:
                        probBetterHand += 1
                probToWin = self.prob_to_win(player, hand_value)
                risk = self.calc_risk(player) * (pot.to_play + player.in_pot) * self.tight
                reward = (probBetterHand * probToWin) * (pot.total-player.in_pot) * self.aggression
                if risk == 0:
                        risk = reward
                #if pot.raised:
                        #risk *= (pot.total/(pot.blinds[0]+pot.blinds[1]))
                #print("Me code: ", probBetterHand)
                #print("Pot to play: ", pot.to_play)
                #print("Pot total: ", pot.total)
                #print("Player in pot: ", player.in_pot)
                #print("Risk: ", risk)
                #print("Reward", reward)
                player.print_cards()
                if reward / risk < 1:
                        player.fold(pot)
                elif probToWin > 0.95:
                        player.bet(pot, int(player.stack/10))
                else:
                        player.check_call(pot)


        def calc_risk(self, player):
                i = 0
                table_cards=[]
                while i < len(player.total_cards)-2:
                        table_cards.append(player.total_cards[i+2])
                        i+=1
                if len(table_cards) == 0:
                        return 0.6 * 0.25
                else:
                        rep, hand_value, tie_break, raw_data = pokerhands.evaluate_hand(table_cards)
                        riskBetterHand = self.risk_better_hand(table_cards, hand_value, player)
                        #print("Op Better Hand: ", riskBetterHand)
                        return riskBetterHand * self.prob_to_win(player, hand_value)

        def prob_to_win(self, player, hand_value):
                #I'm thinking just straight raw values based on the likelihood of getting the handz
                if hand_value == 900:
                        return 0.99999
                elif hand_value >= 800:
                        return 0.99998
                elif hand_value >= 700:
                        return 0.99975
                elif hand_value >= 600:
                        return 0.99855
                elif hand_value >= 500:
                        return 0.996
                elif hand_value >= 400:
                        return 0.97
                elif hand_value >= 300:
                        return 0.95
                elif hand_value >= 200:
                        return 0.925
                elif hand_value >= 100:
                        return 0.6
                else:
                        return 0.25

        def prob_better_hand(self, player, hand_value):
                probability = 0
                if hand_value < 900:
                        probability += self.possibleRoyalFlush(player.total_cards)
                if hand_value < 800:
                        probability += self.possibleStraightFlush(player.total_cards)
                if hand_value < 700:
                        probability += self.possibleFour(player.total_cards, hand_value)
                if hand_value < 600:
                        probability += self.possibleFullHouse(player.total_cards, hand_value)
                if hand_value < 500:
                        probability += self.possibleFlush(player.total_cards)
                if hand_value < 400:
                        probability += self.possibleStraight(player.total_cards)
                if hand_value < 300:
                        probability += self.possibleTrip(player.total_cards, hand_value)
                if hand_value < 200:
                        probability += self.possibleTwoPairs(player.total_cards, hand_value)
                if hand_value < 100:
                        probability += self.possiblePairs(player.total_cards)
                return probability
        def risk_better_hand(self, hand, hand_value, player):
                probability = 0
                if player.hand_value < 900:
                        probability += self.possibleRoyalFlush(hand)
                if player.hand_value < 800:
                        probability += self.possibleStraightFlush(hand)
                if player.hand_value < 700:
                        probability += self.possibleFour(hand, hand_value)
                if player.hand_value < 600:
                        probability += self.possibleFullHouse(hand, hand_value)
                if player.hand_value < 500:
                        probability += self.possibleFlush(hand)
                if player.hand_value < 400:
                        probability += self.possibleStraight(hand)
                if player.hand_value < 300:
                        probability += self.possibleTrip(hand, hand_value)
                if player.hand_value < 200:
                        probability += self.possibleTwoPairs(hand, hand_value)
                if player.hand_value < 100:
                        probability += self.possiblePairs(hand)
                return probability
        def possiblePairs(self, hand):
                probability = (6 / (52 - len(hand))) * (5 - (len(hand) - 2))
                #print("Pair: ", probability)
                return probability

        def possibleTwoPairs(self, hand, hand_value):
                if hand_value < 100:
                        return 0
                if hand[0].rank == hand[1].rank:
                        return 0
                else:
                        probability = (3 / (52 - len(hand))) * (5 - (len(hand) - 2))
                #print("2 Pair: ", probability)
                return probability

        def possibleTrip(self, hand, hand_value):
                probability = 0
                cards_needed = 2
                probCard1 = 0
                probCard2 = 0

                if hand_value > 100:
                        probability = (2 / (52 - len(hand))) * (5 - (len(hand) - 2))
                        #print("Triple: ", probability)
                        return probability

                if cards_needed > (5 - (len(hand) - 2)):
                        return 0
                else:
                        i = 0
                        while i < (5 - (len(hand) - 2)):
                                probCard1 += 3/(52 - len(hand) - i)
                                probCard2 += 2/(52 - len(hand) - i - 1)
                                i = i+1
                        probability = probCard1 * probCard2
               # print("Triple: ",probability)
                return probability

        def possibleStraight(self, hand):
                probability = 0
                cards_needed = self.cardsNeededForStraight(hand)

                if cards_needed > (5 - (len(hand) - 2)):
                        return 0
                else:
                        ##i = 0
                        #while i < cards_needed:
                                #tempProb = 1
                                #j = 0
                                #while j < (5 - (len(hand) - 2)):
                                        #tempProb *= 4/(52 - len(hand) - i)
                                        #j+=1
                                #probability += tempProb
                                #i+=1
                        probability = (pow(self.xChooseY(4,1), cards_needed) / self.xChooseY(52-len(hand), 7-len(hand)))
                #print("Straight: ", probability)
                return probability

        def possibleFlush(self, hand):
                probability = 1
                suits = []
                for card in hand:
                        suits.append(card.suit)
                suit_count = Counter(suits)
                mostCommon = max(suit_count, key=suit_count.get)
                cardsNeeded = 5 - suit_count[mostCommon]
                if cardsNeeded > (7 - len(hand)):
                        return 0
                else:
                        i = 0
                        while i < cardsNeeded:
                                probability *= (13 - suit_count[mostCommon] - i)/(52 - len(hand) - i)
                                i+=1
                #print("Flush: ", probability)
                return probability

        def possibleFullHouse(self, hand, hand_value):
                probability = 0

                if hand_value > 200:
                        i = 0
                        while i < (7 - len(hand)):
                                probability += (6/(52 - len(hand) - i))
                                i+=1
                elif hand_value > 100:
                        i=0
                        cardsNeeded = 2
                        if cardsNeeded > (7 -len(hand)):
                                return 0
                        else:
                                poss1 = 0
                                poss2 = 0
                                while i < (7 - len(hand) - 1):
                                        poss1 += ((3-i) / (52 - len(hand) - i))
                                        i+=1
                                poss1 *= (2 / (52 - len(hand)))
                                i = 0
                                while i < (7 - len(hand)):
                                        poss2 += ((3-i) / (52 - len(hand) - i))
                                        i+=1
                                probability = poss1 + poss2

                else:
                        cardsNeeded = 3
                        if cardsNeeded > (7 -len(hand)):
                                return 0
                        else:
                                i = 0
                                card1 = 1
                                card2 = 1
                                while i < (7 - len(hand)):
                                        card1 *= (3 / (52 - len(hand) - i))
                                        card2 *= (3 / (52 - len(hand) - i - 1))
                                        i += 1
                                probability = (self.possibleTrip(hand, hand_value) * self.possiblePairs(hand))
                #print("Full House: ", probability)
                return probability

        def possibleFour(self, hand, hand_value):
                probability = 1
                cardsNeeded = 4
                if hand_value > 300:
                        cardsNeeded = 1
                elif hand_value > 100:
                        cardsNeeded = 2
                else:
                        cardsNeeded = 3
                if cardsNeeded > (7 - len(hand)):
                        return 0
                else:
                        i = 0
                        while i < cardsNeeded:
                                probability *= ((cardsNeeded-i)/(52 - len(hand) - i))
                                i+=1
                #print("Four: ", probability)
                return probability*2

        def possibleStraightFlush(self, hand):
                probability = 0
                cards_needed = self.cardsForStraightFlush(hand)

                if cards_needed > (7 - len(hand)):
                        return 0
                else:
                        probability = pow((1/(52 - len(hand))), cards_needed)
                #print("Straight Flush: ", probability)
                return probability

        def possibleRoyalFlush(self, hand):
                probability = 0
                if hand[0].value < 9 and hand[1].value < 9:
                        return 0

                cards_needed = self.cardsForRoyalFlush(hand)

                if cards_needed > (7 - len(hand)):
                        return 0

                else:
                        probability = pow((1 / (52 - len(hand))), cards_needed)

                #print("Straight Flush: ", probability)
                return probability


        def cardsNeededForStraight(self, hand):
                cardsNeeded = 4
                if abs(hand[0].value - hand[1].value) < 5:
                        cardsNeeded = 3
                        i = 0
                        dupeCard = []
                        while i < (len(hand) - 2):
                                if abs(hand[i+2].value - hand[0].value) < 5 and abs(hand[i+2].value - hand[1].value) < 5 and hand[i+2].value not in dupeCard:
                                        cardsNeeded = cardsNeeded - 1
                                        dupeCard.append(hand[i+2].value)
                                i += 1
                else:
                        cards_for_hand0 = 4
                        cards_for_hand1 = 4
                        i = 0
                        dupeCard = []
                        while i < (len(hand) - 2):
                                if hand[i+2].value not in dupeCard:
                                        if abs(hand[i + 2].value - hand[0].value) < 5:
                                                cards_for_hand0 -= 1
                                        if abs(hand[i + 2].value - hand[1].value) < 5:
                                                cards_for_hand1 -= 1
                                                dupeCard.append(hand[i+2].value)
                                i += 1
                        cardsNeeded = min(cards_for_hand0, cards_for_hand1)
                        if cardsNeeded < 1:
                                cardsNeeded = 1
                return cardsNeeded

        def cardsForStraightFlush(self, hand):
                cardsNeeded = 4
                if abs(hand[0].value - hand[1].value) < 5 and hand[0].suit == hand[1].suit:
                        cardsNeeded -= 1
                        i = 0
                        while i < (len(hand) - 2):
                                if abs(hand[i + 2].value - hand[0].value) < 5 and abs(hand[i + 2].value - hand[1].value) < 5 and hand[i + 2].suit == hand[0].suit:
                                        cardsNeeded -= 1
                                i += 1
                else:
                        cards_for_hand0 = 4
                        cards_for_hand1 = 4
                        i = 0
                        while i < (len(hand) - 2):
                                if abs(hand[i + 2].value - hand[0].value) < 5 and hand[i + 2].suit == hand[0].suit:
                                        cards_for_hand0 -= 1
                                if abs(hand[i + 2].value - hand[1].value) < 5 and hand[i + 2].suit == hand[0].suit:
                                        cards_for_hand1 -= 1
                                i += 1
                        cardsNeeded = min(cards_for_hand0, cards_for_hand1)
                if cardsNeeded < 1:
                        cardsNeeded = 1

                return cardsNeeded

        def cardsForRoyalFlush(self, hand):
                        cardsNeeded = 4
                        if hand[0].value > 8 and hand[1].value > 8 and hand[0].suit == hand[1].suit:
                                cardsNeeded -= 1
                                i = 0
                                dupedCards = [hand[0].value, hand[1].value]
                                while i < (len(hand) - 2):
                                        if hand[i + 2].value > 8 and hand[i + 2] not in dupedCards and hand[i + 2].suit == hand[0].suit:
                                                cardsNeeded -= 1
                                                dupedCards.append(hand[i + 2].value)
                                        i += 1
                        else:
                                cards_for_hand0 = 4
                                cards_for_hand1 = 4
                                i = 0
                                dupedCards0 = [hand[0].value]
                                dupedCards1 = [hand[1].value]
                                while i < (len(hand) - 2):
                                        if hand[i + 2].value > 8 and hand[i + 2] not in dupedCards0 and hand[i + 2].suit == hand[0].suit:
                                                cards_for_hand0 -= 1
                                                dupedCards0.append(hand[i + 2].value)
                                        if hand[i + 2].value > 8 and hand[i + 2] not in dupedCards1 and hand[i + 2].suit == hand[1].suit:
                                                cards_for_hand1 -= 1
                                                dupedCards1.append(hand[i + 2].value)
                                        i += 1
                                cardsNeeded = min(cards_for_hand0, cards_for_hand1)
                        if cardsNeeded < 1:
                                cardsNeeded = 1
                        return cardsNeeded

        def xChooseY(self, x, y):
                return (math.factorial(x)/(math.factorial(y)*math.factorial(x-y)))
			
class SklanskySys2(Strategy):

        #sklansky all-in tournament strategy

        def decide_play(self, player, pot):

                total_blinds=(pot.blinds[0]+pot.blinds[1])
                score=(player.stack/total_blinds)
                score*=pot.yet_to_play
                score*=(pot.limpers+1)
                score=int(score)
                
                hand_value, rep, tie_break, raw_data=player.get_value()
                raw_values, flush_score, straight, gappers=raw_data
                raw_values.sort()
                
                key=((range(0,19)), (range(20,39)), (range(40,59)), (range(60,79)), (range(80,99)), (range(100,149)), (range(150,199)), (range(200, 399)), (range(400, 1000)))

                for k in key:
                	if score in k:
                		pointer=key.index(k)

                GAI=False

                print ('score='+str(score))
                print ('pot raised='+str(pot.raised))
                
                if pot.raised:

                        if raw_values in ((13,13), (12,12)):
                                GAI=True

                        elif raw_values in (13,12) and flush_score==2:
                                GAI=True

                        else:
                                GAI=False
                
                elif score>400 and raw_values in (13,13):
                        GAI=True
                elif score in range (200,399) and raw_values in ((13,13),(12,12)):
                        GAI=True
                elif score in range (150,199) and raw_values in ((13,13),(12,12), (11,11), (13,12)):
                        GAI=True
                elif score in range (100,149) and raw_values in ((13,13),(12,12),(11,11),(10,10),(9,9),(13,12),(13,11),(12,11)):
                        GAI=True
                elif score in range (80,99):
                        if 'pair' in rep:
                                GAI=True
                        elif raw_values in ((13,12),(13,11),(12,11)):
                                GAI=True
                        elif flush_score==2 and 13 in raw_values:
                                GAI=True
                        elif flush_score==2 and straight>=5:
                                GAI=True
                elif score in range (60,79):
                        if 'pair' in rep:
                                GAI=True
                        elif 13 in raw_values:
                                GAI=True
                        elif flush_score==2 and 12 in raw_values:
                                GAI=True
                        elif flush_score==2 and gappers<=1:
                                GAI=True
                elif score in range (40,59):
                        if 'pair' in rep:
                                GAI=True
                        elif 13 or 12 in raw_values:
                                GAI=True
                        elif flush_score==2 and 12 in raw_values:
                                GAI=True
                        elif flush_score==2 and gappers<=1:
                                GAI=True
                elif score in range (20,39):
                        if 'pair' in rep:
                                GAI=True
                        elif 13 or 12 in raw_values:
                                GAI=True
                        elif flush_score==2:
                                GAI=True
                elif score in range(0,19):
                        GAI=True

                else:
                        GAI=False


                if GAI:
                        if player.stack<=player.to_play:
                                player.check_call(pot)
                        else:
                                player.bet(pot, player.stack)
                else:
                        player.fold(pot)
                        
                        
                

##Key Number = 400 or more: Move in with AA and fold everything else.
##Key Number = 200 to 400: Move in with AA and KK only.
##Key Number = 150 to 200: Move in with AA, KK, QQ and AK
##Key Number = 100 to 150: Move in with AA, KK, QQ, JJ, TT, AK, AQ and KQ
##Key Number = 80 to 100: Move in with any pair, AK, AQ, KQ, any suited Ace and
##any suited connector down to 5-4 suited.
##Key Number = 60 to 80: Move in with any pair, any ace, KQ, any suited king
##and all one-gap and no-gap suited connectors.
##Key Number = 40 to 60: Move in with everything above + any king.
##Key Number = 20 to 40: Move in with everything above + any 2 suited cards
##Key Number = <20: Move in with any 2-cards.


class Random(Strategy):

    
        def decide_play(self, player, pot):

                
             
                choice=random.randint(0,3)
               
                
                if choice==0:
                	player.fold(pot)
                
                elif choice==1:
                	if player.stack<=player.to_play:
                		player.check_call(pot)
                	else:
                		player.bet(pot, calc_bet(player))
                elif choice==2:
                	if player.stack<=player.to_play:
                		player.check_call(pot)
                	else:
                		player.bet(pot, player.stack)


class AllIn(Strategy):

        def decide_play(self, player, pot):

                if player.stack <= player.to_play:
                        player.check_call(pot)
                else:
                        player.bet(pot, player.stack)
                
                
		
class Human(Strategy):
    
    options=[['x', 'f', 'b'], ['c', 'r', 'f'], ['c', 'f']]
    choices={0:'check, fold or bet', 1:'call, raise, fold', 2:'call all-in or fold'}
    
    def decide_play(self, player, pot):
        
        player.get_value()
        
        options=Human.options
        choices=Human.choices
        action=''
        op=0


        if player.to_play==0:
                op=0
        elif player.to_play<player.stack:
                op=1
        else: op=2

        

        while action not in options[op]:

                try:
                        action=input(str(choices[op]))
                except NameError:
                 print ('enter a valid choice')

    
        if action=='x':
                player.check_call(pot)
        elif action=='f':
                player.fold(pot)
        elif action=='c':
                player.check_call(pot)
        elif action=='b' or action=='r':
                stake=0
                max_bet=player.stack
                print ('max '+str(max_bet))
                while stake not in range (10,(max_bet+1), 5):
                        try:
                                stake=int(input('stake..'))
                        except:
                                print ('input a stake')
                print ('stake '+str(stake))                                
                player.bet(pot, stake)

        
class Fish(Strategy):
        
        def decide_play(self, player, pot):
                
                if player.to_play == 0:
                        if player.stack >= 10:
                                player.bet(pot, 10)               
                        else:        
                                player.fold(pot)
                elif player.stack <= player.to_play:
                        player.check_call(pot)
                else:
                        player.bet(pot, player.to_play)
	
class LionFish(Strategy):
        
        def decide_play(self, player, pot):
                
                if player.to_play == 0:
                        if player.stack >= 10:
                                player.bet(pot, 10)               
                        else:        
                                player.fold(pot)
                else:   
                        if(player.get_value()[0] >= 900):
                                player.bet(pot, player.stack) 
                        elif(player.get_value()[0] >= 800):
                                player.bet(pot, player.stack/2) 
                        elif(player.get_value()[0] >= 700):
                                player.bet(pot, player.stack/3) 
                        elif(player.get_value()[0] >= 600):
                                player.bet(pot, player.stack/4) 
                        elif(player.get_value()[0] >= 500):
                                player.bet(pot, player.stack/5) 
                        elif(player.get_value()[0] >= 400):
                                player.bet(pot, player.stack/6)              
                        elif(player.get_value()[0] >= 300):
                                player.bet(pot, player.stack/7)                        
                        elif(player.get_value()[0] >= 200):
                                player.bet(pot, player.stack/8) 
                        elif(player.get_value()[0] >= 100):
                                player.bet(pot, player.stack/9) 
                                        
                        elif player.stack <= player.to_play:
                                player.check_call(pot)
                        else:
                                player.bet(pot, player.to_play)             
		
			
			
			
			
		
	
	
	


