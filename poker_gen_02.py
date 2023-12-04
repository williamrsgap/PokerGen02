import random, os
    
class Mister_House:
    class Player:
        def __init__(self):
            self.name = "Courier"
            self.folded = False
            self.money = 0
            self.hand = [[None,None],[None,None]]

        # raise (force raise for initial bet)
        def up_bet(self,house,n):
            house.bet += n
            self.money -= n
            
        # call
        def same_bet(self,house):
            self.money -= house.bet
        
        # fold
        def quitter(self):
            self.folded = True
        
    class agent(Player):
        #ai
        def request_action(self,house):
            pass
    
    class user(Player):
        #user
        def request_action(self,house):
            if house.bet == 0:
                req_init_bet()
            else:
                req_play()
        def req_init_bet(self,house):
            #ask the player for an initial bet through Maestro Class
            pass
        def req_play(self,house):
            #ask the player to raise, call, or fold
            pass
            
    class Maestro:
        # orecstrate all ui
        class Page:
            def __init__(self,name: str,desc: str,ops):
                self.name = name # page title (string)
                self.desc = desc # description (string)
                self.ops = ops # user options ([[option name,function]])
        class Game(Page):
            pass
        
        def __init__(self):
            self.uni_cmds = {
                "help":self.help,
                "quit":exit
            }
            self.Main = Page("Main Menu","The starting menu",{
                "play":[self.new_page,self.game_start],
                "statistics":[self.new_page,self.stats]})
            self.stats = Page("Statistics","Play Stats",{
                "back":[self.new_page,self.Main]})
            self.game_start = Game("Setup","Declare starting money and ai count",{})
            self.active_page = self.Main
        
        def new_page(self,move_to: Page): #load new page and get next move
            os.system('clr')
            self.active_page = move_to
            print(move_to.name+"\n\n\n\n")
            print("Options\n\n")
            for i in move_to.ops:
                print(str.capitalize(i)+" | ",end="")
            while(True):
                nextm = input("Select an option:\n")
                try:
                    temp = move_to.ops[nextm]
                    temp[0](temp[1])
                    break
                except:
                    try:
                        return self.uni_cmds[str.lower(nextm)]()
                    except:
                        print("Invalid Option, Try Again\n\n")
                    continue
        def help(self,page):
            print("NAME:  "+page.name+"\n")
            print("DESCRIPTION:  "+page.desc+"\n")
            print("Options\n")
            for i in move_to.ops:
                print(str.capitalize(i)+" | ",end="")
            print("\n\n\n")
                
    def __init__(self):
        self.players = []  # all player
        self.bank = 0 # house monet=y
        self.bet = 0 # current bet on the table
        self.turn = 0 #current turn
        self.max_turn = 0 # last person
        self.table_cards = [None] * 5 # values of cards on the table 
        self.cards_flipped = [False] * 5 # which cards are face up 
        self.deck = [None]*52 # the current deck
        self.deck_place = 0 # which card is on top
        
        # define cards and suits
        self.TYPE = [
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
            "jack",
            "queen",
            "king",
            "ace"]
        self.SUIT=[
            "heart",
            "club",
            "diamond",
            "spade"] 
    
    def setup(self,bank_value,init_cash,players):
        self.players = players
        self.bank = bank_value
        self.max_turn = len(players) -1

        # set player initial cashes
        for i in self.players:
            i.money = init_cash
    
    def draw():
    #draw top card
        temp = self.deck[self.deck_place]
        self.deck_place+=1
        return temp

    def create_deck():
    # create an empty deck
        deck = [] 
        # iterate through each card
        for i in range(len(self.SUIT)):
            for j in range(len(self.TYPE)):
                deck[i*14+j] = [i,j]
        # give it out
        return random.shuffle(deck)
        
    def deal():
        # shuffle
        self.deck = create_deck()
        # dealt to players
        for i in self.players:
            i.hand = [self.draw(),self.draw()]
        # placed on table
        for i in self.table_cards:
            i = self.draw()
        # flip first three
        self.cards_flipped = [True,True,True,False,False]
    
    def all_turn(self):
        for i in self.players:
            if i.folded == False:
                i.requset_action()