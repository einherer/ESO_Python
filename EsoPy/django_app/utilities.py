import luadata
from django_app.models import Server, Account, Character, Equipment, ActiveAbility, ActiveBuff


def read_lua(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lua_content = file.read()
    return luadata.unserialize(lua_content)

def load_data_into_database(lua_data):
    for server_name, server_data in lua_data.items():
        server, _ = Server.objects.get_or_create(name=server_name)
        for account_name, account_data in server_data.items():
            account, _ = Account.objects.get_or_create(server=server, name=account_name)
            for character_id, character_data in account_data.items():
                character, _ = Character.objects.get_or_create(
                    account=account,
                    character_id=character_id,
                    name=character_data.get('Name', ''),
                    faction_name=character_data.get('FactionName', ''),
                    race_name=character_data.get('RaceName', ''),
                    class_name=character_data.get('ClassName', ''),
                    level=character_data.get('Level', 0),
                    champion_points=character_data.get('ChampionPoints', 0),
                    is_werewolf=character_data.get('isWerewolf', False),
                    is_vampire=character_data.get('isVampire', False)
                )
                #### TODO save equipment, active abilities and active buffs

def print_lua(lua_data):
    for server_name, server_data in lua_data.items():
        print(server_name)
        for account_name, account_data in server_data.items():
            print(account_name)
            for character_id, character_data in account_data.items():
                print(character_id)
                for key, value in character_data.items():
                    if key == 'Equipment':
                        for item in value:
                            print(item['name'])
                            print(item['slot'])
                            print(item['icon'])
                            print(item['quality'])
                    elif key == 'ActiveAbilities':
                        for ability in value:
                            print(ability['name'])
                            print(ability['description'])
                            print(ability['icon'])
                    elif key == 'ActiveBuffs':
                        for buff in value:
                            print(buff['name'])
                            print(buff['description'])
                            print(buff['icon'])
                    else:
                        print(f"{key} : {value}")

if __name__ == '__main__':
    file_path = '..\..\..\SavedVariables\MyOwn.lua'
    lua_data = read_lua(file_path)
    print_lua(lua_data)
    #load_data_into_database(lua_data)