local addonName = "MyOwn"
local appversion = 1.20240523

MyOwn = {}
MyOwn.SaveVars = {}
MyOwn.Helpers = {}

-- Initialize saved variables
function MyOwn.InitializeSavedVars()
    local defaults = {
        Name = "",
        FactionName = "",
        RaceName = "",
        ClassName = "",
        Level = 0,
        ChampionPoints = 0,
        isWerewolf = false,
        isVampire = false,
        Equipment = {
            slot = "",
            name = "",
            itemLink = "",
            quality = "",
            icon = "",
            SetInfo = "",
            SetBonusInfo = "",
            EnchantInfo = "",
        },
        activeAbilities = {
            id = 0,
            name = "",
            description = "",
            icon = "",
        },
        activeBuffs = {
            id = 0,
            name = "",
            description = "",
            icon = "",
        },
    }
    MyOwn.SaveVars = ZO_SavedVars:NewCharacterIdSettings('MyOwnSavedVars', appversion, nil, defaults, GetWorldName())
end

-- Function to save character data to saved variables
function MyOwn.SaveCharacterData()
    MyOwn.SaveVars.Name = GetUnitName("player")
    MyOwn.SaveVars.ClassName = string.gsub(GetUnitClass("player"), "%^.", "")
    MyOwn.SaveVars.RaceName = string.gsub(GetUnitRace("player"), "%^.", "")
    MyOwn.SaveVars.FactionName = MyOwn.Helpers.GetFactionName()
    MyOwn.SaveVars.Level = GetUnitLevel("player")
    MyOwn.SaveVars.ChampionPoints = GetPlayerChampionPointsEarned()
    MyOwn.SaveVars.isWerewolf = MyOwn.Helpers.IsWerewolf()
    MyOwn.SaveVars.isVampire = MyOwn.Helpers.IsVampire()
    MyOwn.SaveVars.Equipment = MyOwn.Helpers.GetEquippedItems()
    MyOwn.SaveVars.activeAbilities = MyOwn.Helpers.GetActiveAbilities()
    MyOwn.SaveVars.activeBuffs = MyOwn.Helpers.GetActiveBuffs()
end

-- Function to print the saved character data to the chat
function MyOwn.PrintCharacterDataToChat()
    if MyOwn.SaveVars.CharacterData then
        d("Character Name: " .. MyOwn.SaveVars.Name)
        d("Class: " .. MyOwn.SaveVars.ClassName)
        d("Race: " .. MyOwn.SaveVars.RaceName)
        d("Faction: " .. MyOwn.SaveVars.FactionName)
        d("Character Level: " .. tostring(MyOwn.SaveVars.Level))
        d("Champion Points: " .. tostring(MyOwn.SaveVars.ChampionPoints))
        d("Is Vampire: " .. tostring(MyOwn.SaveVars.isVampire))
        d("Is Werewolf: " .. tostring(MyOwn.SaveVars.isWerewolf))
        -- Print Equipment
        d("Equipped Items:")
        for _, equipment in ipairs(MyOwn.SaveVars.Equipment) do
            d("Slot: " .. equipment.slot)
            d("Name: " .. equipment.name)
            d("Item Link: " .. equipment.itemLink)
            d("Quality: " .. equipment.quality)
            d("icon: " .. equipment.icon)
            d("Set Info: " .. equipment.SetInfo)
            d("Set Bonus Info: " .. equipment.SetBonusInfo)
            d("Enchant Info: " .. equipment.EnchantInfo)
            d("-------------------------------")
        end
        -- Print active abilities
        d("Active Abilities:")
        for _, ability in ipairs(MyOwn.SaveVars.activeAbilities) do
            d("- " .. ability.name .. " (ID: " .. tostring(ability.id) .. ")")
        end
        -- Print active buffs
        d("Active Buffs:")
        for _, buff in ipairs(MyOwn.SaveVars.activeBuffs) do
            d("- " .. buff.name .. " (ID: " .. tostring(buff.id) .. ")")
        end
    else
        d("No character data found.")
    end
end
-- #################### Helper Functions #####################
MyOwn.Helpers.factionNames = {
    [ALLIANCE_ALDMERI_DOMINION] = "Aldmeri Dominion",
    [ALLIANCE_EBONHEART_PACT] = "Ebonheart Pact",
    [ALLIANCE_DAGGERFALL_COVENANT] = "Daggerfall Covenant"
}
MyOwn.Helpers.slotNames = {
    [0] = "Head",
    [1] = "Neck",
    [2]= "Chest",
    [3] = "Shoulders",
    [4] = "Main Hand",
    [5] = "Off Hand",
    [6] = "Waist",
    [7] = "7",
    [8] = "Legs",
    [9]= "Feet",
    [10] = "Costume",
    [11] = "Ring 1",
    [12] = "Ring 2",
    [13] = "Main Poison",
    [14] = "Backup Poisen",
    [15] = "15",
    [16] = "Gloves",
    [17] = "17",
    [18] = "18",
    [19] = "19",
    [20] = "Backup Main Hand",
    [21] = "Backup Off Hand",
}
MyOwn.Helpers.qualities = {
    [0] = "?",
    [1] = "normal",
    [2] = "fine",
    [3] = "superior",
    [4] = "epic",
    [5] = "legendary",
    [6] = "artifact",
    [7] = "mythic",
}

function MyOwn.Helpers.GetFactionName()
    local alliance = GetUnitAlliance("player")
    return MyOwn.Helpers.factionNames[alliance] or "Unknown"
end

function MyOwn.Helpers.IsVampire()
    local vampireAbilityIds = {135397, 135398, 135399, 135400}
    for i = 1, GetNumBuffs("player") do
        local buffName, _, _, _, _, _, _, _, _, _, abilityId = GetUnitBuffInfo("player", i)
        if MyOwn.Helpers.Contains(vampireAbilityIds, abilityId) or string.find(buffName, "Vampir") then
            return true
        end
    end
    return false
end

function MyOwn.Helpers.IsWerewolf()
    local WolfAbilityIds = 35658
    for i = 1, GetNumBuffs("player") do
        local _, _, _, _, _, _, _, _, _, _, abilityId = GetUnitBuffInfo("player", i)
        if abilityId == WolfAbilityIds then
            return true
        end
    end
    return IsWerewolf()
end

function MyOwn.Helpers.Contains(table, value)
    for _, v in ipairs(table) do
        if v == value then
            return true
        end
    end
    return false
end

function MyOwn.Helpers.GetEquippedItems()
    local equippedItems = {}

    for slotId, slotName in pairs(MyOwn.Helpers.slotNames) do
        local itemLink = GetItemLink(BAG_WORN, slotId)
        if itemLink ~= "" then
            local hasSet, setName, numBonuses, numEquipped, maxEquipped = GetItemLinkSetInfo(itemLink)
            local setBonusText = ""
            if hasSet then
                for i = 1, numBonuses do
                    local _, bonusDescription = GetItemLinkSetBonusInfo(itemLink, EQUIPPED, i)
                    setBonusText = setBonusText .. bonusDescription .. "\n"
                end
            else
                setName = ""
            end

            local ehas, ename, einfo = GetItemLinkEnchantInfo(itemLink)
            if ehas then
                einfo = ename .. " " .. einfo
            else
                einfo = ""
            end

            local equipmentData = {
                slot = slotName,
                name = GetItemLinkName(itemLink),
                itemLink = itemLink,
                quality = MyOwn.Helpers.qualities[GetItemLinkQuality(itemLink)],
                icon = GetItemLinkInfo(itemLink),
                SetInfo = setName,
                SetBonusInfo = setBonusText,
                EnchantInfo = einfo,
            }
            table.insert(equippedItems, equipmentData)
        end
    end

    return equippedItems
end

function MyOwn.Helpers.GetActiveAbilities()
    local abilities = {}
    -- Save active abilities from the active bar
    for i = 3, 8 do -- 1 and 2 are light and heavy attack
        local abilityId = GetSlotBoundId(i)
        local abilityName = GetAbilityName(abilityId)
        local formattedString = string.gsub(abilityName, "%^.", "")
        local abilityDescription = GetAbilityDescription(abilityId)
        local abilityIcon = GetAbilityIcon(abilityId)
        table.insert(abilities, {id = abilityId, name = formattedString, description = abilityDescription, icon = abilityIcon})
    end

    return abilities
end

function MyOwn.Helpers.GetActiveBuffs()
    local buffs = {}
    -- Save active buffs
    for i = 1, GetNumBuffs("player") do
        local buffName, startTime, endTime, buffSlot, stackCount, iconFilename, buffType, effectType, abilityType, statusEffectType, abilityId, canClickOff = GetUnitBuffInfo('player', i)
        local buffDescription = GetAbilityDescription(abilityId)
        local formattedString = string.gsub(buffName, "%^.", "")
        table.insert(buffs, {id = abilityId, name = formattedString, description = buffDescription, icon = iconFilename})
    end

    return buffs
end
-- #################### Event handlers #######################
local function CollectAndPrint()
    MyOwn.SaveCharacterData()
    MyOwn.PrintCharacterDataToChat()
end

local function OnPlayerActivated(eventCode)
    MyOwn.SaveCharacterData()
end

local function OnPlayerDeactivated(eventCode)
    MyOwn.SaveCharacterData()
end

-- Initialize the addon
local function OnAddonLoaded(eventCode, addonNameLoaded)
    if addonNameLoaded == addonName then
        MyOwn.InitializeSavedVars()
        EVENT_MANAGER:RegisterForEvent(addonName, EVENT_PLAYER_ACTIVATED, OnPlayerActivated)
        EVENT_MANAGER:RegisterForEvent(addonName, EVENT_PLAYER_DEACTIVATED, OnPlayerDeactivated)
        SLASH_COMMANDS["/myown"] = CollectAndPrint
        EVENT_MANAGER:UnregisterForEvent(addonName, EVENT_ADD_ON_LOADED)
    end
end

EVENT_MANAGER:RegisterForEvent(addonName, EVENT_ADD_ON_LOADED, OnAddonLoaded)
