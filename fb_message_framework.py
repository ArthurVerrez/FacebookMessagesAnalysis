from datetime import datetime
import json
import copy
from matplotlib import pyplot as plt


class Conversation():
    path=""
    participants=[]
    messages=[]

    def __init__(self, path):
        self.path = path
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        
        for i in range(len(data["messages"])):
            if("content" in data["messages"][i]):
                m=data["messages"][i]["content"]
                data["messages"][i]["content"]=bytes(m, "latin-1").decode("utf-8")
                
        for i in range(len(data['participants'])):
            self.participants.append(Person(data['participants'][i]["name"], i))
        
        for i in range(len(data["messages"])):
            sender=None
            time=datetime(2019, 1,1)
            content=""
            has_photo=False
            has_gif=False
            has_reaction=False
            reactions=[]
            photos=[]
            gifs=[]
            if("sender_name" in data["messages"][i]):
                sender=self.id_participant_name(data["messages"][i]["sender_name"])
                
            if("timestamp_ms" in data["messages"][i]):
                time=datetime.fromtimestamp(data['messages'][i]['timestamp_ms']/1000)
            if("content" in data["messages"][i]):
                content=data["messages"][i]["content"]
            if("photos" in data["messages"][i]):
                has_photo=True
                for j in range(len(data["messages"][i]["photos"])):
                    photos.append(data["messages"][i]["photos"][j]["uri"])
            if("gifs" in data["messages"][i]):
                has_gif=True
                for j in range(len(data["messages"][i]["gifs"])):
                    gifs.append(data["messages"][i]["gifs"][j]["uri"])
                    
            if("reactions" in data["messages"][i]):
                has_gif=True
                for j in range(len(data["messages"][i]["reactions"])):
                    reactions.append(Reaction(self.id_participant_name(data["messages"][i]["reactions"][j]["actor"]), data["messages"][i]["reactions"][j]["reaction"]))
            
            
            self.messages.append(Message(sender, time, content, has_photo, has_gif, has_reaction, reactions, photos, gifs))
    
    #Returns the id of the participant with the name name
    def id_participant_name(self, name):
        for i in range(len(self.participants)):
            if(self.participants[i].name==name):
                return self.participants[i]
        return None
        
    #Returnes the conversation with only the messages between the specified datetimes
    def getConversation(self, start=datetime(1, 1, 1, 0, 0), end=datetime.now()):
        conv=copy.deepcopy(self)
        conv.messages=[]
        for m in self.messages:
            if(m.time>=start and m.time<end):
                conv.messages.append(copy.deepcopy(m))
        return conv
    
    #Returns the dates of the messages of the participants as an array
    #dates[participant_id][i] = datetime of the i_th message of the participant whose id is participant_id
    def getMessagesDates(self):
        dates=[[] for k in range(len(self.participants))]
        for m in self.messages:
            dates[m.sender.id].append(m.time)
        return dates
    
    #Return the dates of the messages as an array
    def getMessagesDatesTotal(self):
        dates=[]
        for m in self.messages:
            dates.append(m.time)
        return dates
            
    
    #Show a graph with the cumulative number of messages for each participants over time
    def showGraphMessagesDates(self):
        dates=self.getMessagesDates()
        
        for i in range(len(dates)):
            plt.plot_date(dates[i], [k for k in range(len(dates[i]))][::-1], label=self.participants[i].name, marker='None', linestyle="-")
            
        plt.title("Cumulative number of messages for each participants over time")
        plt.xlabel('Date')
        plt.ylabel('Cumulative number of messages')

        plt.legend()
        
        plt.show()
    
    def showGraphMessagesDatesTotal(self):
        dates=self.getMessagesDatesTotal()
        
        plt.plot_date(dates[i], [k for k in range(len(dates))][::-1], label="Messages count", marker='None', linestyle="-")
            
        plt.title("Cumulative number of messages over time")
        plt.xlabel('Date')
        plt.ylabel('Cumulative number of messages')

        plt.legend()
        
        plt.show()
    
        
class Person():
    name=""
    id=0
    def __init__(self, name, id):
        self.name=name
        self.id=id
    
class Message():
    sender=None
    time=datetime(2019, 1,1)
    content=""
    has_photo=False
    has_gif=False
    has_reaction=False
    reactions=[]
    photos=[]
    gifs=[]
    
    def __init__(self, sender, time, content, has_photo, has_gif, has_reaction, reactions, photos, gifs):
        self.sender=sender
        self.time=time
        self.content=content
        self.has_photo=has_photo
        self.has_gif=has_gif
        self.has_reaction=has_reaction
        self.reactions=reactions
        self.photos=photos
        self.gifs=gifs

    

class Reaction():
    sender=None
    reaction=""
    
    def __init__(self, sender, reaction):
        self.sender=sender
        self.reaction=reaction

conv = Conversation("C:/Users/Arthur Verrez/Drive/Projets/Programmation/Python/MessengerAnalysis/message.json")