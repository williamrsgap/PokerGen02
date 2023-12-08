import random, os
    
class Mister_House:
    class Player:
        def __init__(self,name,money=0):
            self.name = name
            self.folded = False
            self.money = money
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
        
    class agent(self.Player):
        #ai
        def request_action(self,house):
            pass
    
    class user(self.Player):
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
        
        
    
    def setup(self,bank_value,players):
        self.players = players
        self.bank = bank_value
        self.max_turn = len(players) -1

    
    def draw():
    #draw top card
        temp = self.deck[self.deck_place]
        self.deck_place+=1
        return temp

    def create_deck():
    # create an empty deck
        deck = [] 
        # iterate through each card
        for i in range(4):
            for j in range(13):
                deck[i*13+j] = [i,j]
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
    
    def get_river(self):
        temp = []
        for i in range(len(self.table_cards)):
            if self.cards_flipped[i]:
                temp.append(self.table_cards[i])
        return temp
          
class Maestro:
    # orecstrate all ui
    class Page:
        def __init__(self,name: str,desc: str,ops):
            self.name = name # page title (string)
            self.desc = desc # description (string)
            self.ops = ops # user options ([[option name,function]])
            
    class Game(Page):
        def setup_prompts(self,house: Mister_House):
            s_money = self.get_int_from_player("How much money should players start with?\n","Thats not a valid integer. Try again")            
            h_money = self.get_int_from_player("How much money should the house start with?\n","Thats not a valid integer. Try again")            
            peep_n = self.get_int_from_player("How many People are playing?\n","Thats not a valid integer. Try again")
            computer_n = self.get_int_from_player("How many Computers are playing?\n","Thats not a valid integer. Try again")
            
            users = []
            for i in range(peep_n):
                users.append(house.user("Player "+str(i),s_money))
                
            comps = []
            for i in range(computer_n):
                users.append(house.agent("Computer "+str(i),s_money))
                
            players = random.shuffle(users + comps)
            
            house.setup(h_money,players)
                                    
        def get_int_from_player(self,request: str,fail: str):
            while(True):
                try:
                    return int(input(request))
                    break
                except:
                    print(fail)
                    continue
        def get_move_from_player(self,house: Mister_House,player):
            os.system('clr')
            print("River:\n\n")
            river_str = ""
            temp = house.get_river
            for i in get_river:
                pass # get type and string and add it to the master string with spacing
            
            # print that big string out
            # ask player for his move
            #differuiniate intial move and in play
            
            
    def __init__(self):
        self.uni_cmds = { # commands usable on all screens
            "help":self.help,
            "quit":exit
        }
        self.Main = self.Page("Main Menu","The starting menu",{ # starting page
            "play":[self.new_page,self.game_start],
            "statistics":[self.new_page,self.stats]})
        self.stats = self.Page("Statistics","Play Stats",{ # stats page
            "back":[self.new_page,self.Main]})
        self.game_start = self.Game("Setup","Declare starting money and ai count",{}) # game holding page
        self.active_page = self.Main # set the initial page to the main menu
        
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
    
    def new_page(self,move_to: Page): #load new page and get next move
        os.system('clr')
        self.active_page = move_to
        print(move_to.name+"\n\n\n\n")
        print("Options\n\n")
        for i in move_to.ops:
            print(str.capitalize(i)+" | ",end="")
        if type(move_to) == self.Page:
            while(True):
                nextm = str.lower(input("Select an option:\n"))
                try:
                    temp = move_to.ops[nextm]
                    temp[0](temp[1])
                    break
                except:
                    try:
                        if nextm == 'help':
                            self.uni_cmds[nextm](move_to)
                            break
                        else:
                                self.uni_cmds[nextm]()
                                break
                    except:
                        print("Invalid Option, Try Again\n\n")
                        continue
            else:
                self.play_game()
                    
        def help(self,page): # print info of current page
            print("NAME:  "+page.name+"\n")
            print("DESCRIPTION:  "+page.desc+"\n")
            print("Options\n")
            for i in move_to.ops:
                print(str.capitalize(i)+" | ",end="")
            print("\n\n\n")