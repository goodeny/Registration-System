import json

class System:
    def __init__(self):
        #self.update_id()
        #self.insert(0, "3user", "3")
        #self.update_id()
        #self.load()
        #self.register()
        #print(self.get_data_user(4))
        #print(self.get_all_users())
        #self.delete_user(1)
        pass

    def load(self):
        with open("data.json", "r+") as f:
            data = json.load(f)
        return data
    
    def insert(self, id, name, second_name):
        data = self.load()
        data["data"].append([id, name, second_name])
        with open("data.json", "w") as f:
            json.dump(data, f)
        self.update_id()
        
    def update_id(self):
        data = self.load()
        for i in range(1, len(data["data"])+1):
            data["data"][i-1][0] = i
        with open("data.json", "w") as f:
            json.dump(data, f)

    def get_data_user(self, id):
        self.update_id()
        data = self.load()
        for i in data["data"]:
            id_user = i[0]
            if id_user == id:
                return i
    
    def get_all_users(self):
        self.update_id()
        data = self.load()
        all_users = []
        for i in data["data"]:
            all_users.append(i)
        return all_users

    def delete_user(self, id):
        data = self.load()
        user = self.get_data_user(id)
        all_users = self.get_all_users()
        if user in all_users:
            data["data"].pop((id-1))
            print(f"{user} was deleted")
            with open("data.json", "w") as f:
                json.dump(data, f)
            self.update_id()

if __name__ == "__main__":
    System()
