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
                # Debug prints
                print(f"Processing Character ID: {character_id}")
                print(f"Character Data: {character_data}")

                # Convert values to appropriate types and handle missing data
                level = int(character_data.get('Level', 0))
                champion_points = int(character_data.get('ChampionPoints', 0))
                is_werewolf = bool(character_data.get('isWerewolf', False))
                is_vampire = bool(character_data.get('isVampire', False))

                character, created = Character.objects.get_or_create(character_id=character_id, defaults={
                    'account': account,
                    'name': character_data.get('Name', ''),
                    'faction_name': character_data.get('FactionName', ''),
                    'race_name': character_data.get('RaceName', ''),
                    'class_name': character_data.get('ClassName', ''),
                    'level': level,
                    'champion_points': champion_points,
                    'is_werewolf': is_werewolf,
                    'is_vampire': is_vampire
                })
                if not created:
                    character.account = account
                    character.name = character_data.get('Name', character.name)
                    character.faction_name = character_data.get('FactionName', character.faction_name)
                    character.race_name = character_data.get('RaceName', character.race_name)
                    character.class_name = character_data.get('ClassName', character.class_name)
                    character.level = level
                    character.champion_points = champion_points
                    character.is_werewolf = is_werewolf
                    character.is_vampire = is_vampire
                    character.save()

                # Save equipment
                for equipment_data in character_data.get('Equipment', []):
                    Equipment.objects.update_or_create(
                        character=character,
                        slot=equipment_data['slot'],
                        defaults={
                            'name': equipment_data['name'],
                            'icon': equipment_data['icon'],
                            'quality': equipment_data['quality']
                        }
                    )

                # Save active abilities
                for ability_data in character_data.get('ActiveAbilities', []):
                    ActiveAbility.objects.update_or_create(
                        character=character,
                        name=ability_data['name'],
                        defaults={
                            'description': ability_data['description'],
                            'icon': ability_data['icon']
                        }
                    )

                # Save active buffs
                for buff_data in character_data.get('ActiveBuffs', []):
                    ActiveBuff.objects.update_or_create(
                        character=character,
                        name=buff_data['name'],
                        defaults={
                            'description': buff_data['description'],
                            'icon': buff_data['icon']
                        }
                    )

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