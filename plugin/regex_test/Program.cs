using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

class T
{
    static readonly HashSet<string> LabelWithValueKeys = new HashSet<string>
    {
        "Return To Base", "Search For Convoy", "Break Blockade", "Defend Island",
        "Destroy Vehicles", "Detected units", "Repaired unit", "Take Off", "Taxi",
        "Taxi to Runway", "Cleared for landing on Runway", "Cleared to taxi to Runway",
        "Successful Sortie +"
    };

    static readonly Dictionary<string, string> Tr = new Dictionary<string, string>
    {
        { "Return To Base", "Возврат на базу" },
        { "Search For Convoy", "Поиск конвоя" },
        { "Break Blockade", "Прорыв блокады" },
        { "Defend Island", "Оборона острова" },
        { "Destroy Vehicles", "Уничтожение техники" },
        { "Detected units", "Обнаружено единиц" },
        { "Repaired unit", "Отремонтировано единиц" },
        { "Take Off", "Взлёт" },
        { "Taxi", "Руление" },
        { "Taxi to Runway", "Руление к ВПП" },
        { "Cleared for landing on Runway", "Разрешение на посадку, ВПП" },
        { "Cleared to taxi to Runway", "Разрешение на руление, ВПП" },
        { "Successful Sortie +", "Успешный вылет +" }
    };

    static readonly Regex LabelValueRe = new Regex(
        "^(?<label>.+?)\\s(?<value>[+\\-]?\\d[\\d.,]*(?:\\s?(?:km|m|nm|kt|ft|s|min))?)$",
        RegexOptions.Compiled);
    static readonly Regex BaseNumberRe = new Regex("^(?<base>.+)\\s(?<num>\\d{1,3})$", RegexOptions.Compiled);
    static readonly Regex EndGameKickRe = new Regex(
        "^Are you sure you want to end the game\\? Doing so will kick (\\d+) other players?\\.$", RegexOptions.Compiled);

    static string PluralPlayers(string count)
    {
        int num;
        if (!int.TryParse(count, out num)) return "игроков";
        if (num % 10 == 1 && num % 100 != 11) return "игрока";
        return "игроков";
    }

    static string TryLabelWithValue(string text)
    {
        Match match = LabelValueRe.Match(text);
        if (!match.Success) return null;
        string text2 = match.Groups["label"].Value;
        string text3 = match.Groups["value"].Value;
        if (LabelWithValueKeys.Contains(text2))
        {
            if (Tr.ContainsKey(text2)) return Tr[text2] + " " + text3;
            return null;
        }
        Match match2 = BaseNumberRe.Match(text2);
        if (match2.Success)
        {
            string text4 = match2.Groups["base"].Value;
            if (LabelWithValueKeys.Contains(text4) && Tr.ContainsKey(text4))
                return Tr[text4] + " " + match2.Groups["num"].Value + " " + text3;
        }
        return null;
    }

    static string TryPatternMatch(string text)
    {
        Match match = EndGameKickRe.Match(text);
        if (match.Success)
            return "Вы уверены, что хотите завершить игру? Это исключит из игры " + match.Groups[1].Value + " " + PluralPlayers(match.Groups[1].Value) + ".";
        return TryLabelWithValue(text);
    }

    static void Main()
    {
        string[] cases = {
            "Return To Base 1,4km", "Search For Convoy 10,0km", "Taxi to Runway 01 461m",
            "Cleared for landing on Runway 01", "Cleared to taxi to Runway 34",
            "Detected units +1,0", "Repaired unit +0,3", "Successful Sortie + 52,5",
            "Take Off 715m", "Taxi 85m", "Break Blockade 1,7km", "Defend Island 1,0km",
            "Are you sure you want to end the game? Doing so will kick 1 other players.",
            "Are you sure you want to end the game? Doing so will kick 5 other players.",
            "Are you sure you want to end the game? Doing so will kick 0 other players.",
            "RNG 1,0km", "REL -0,1m", "ALT 1000m", "MAX 8,3km", "V -1,9", "ETA 15,3s",
            "AFV8 APC +2,3", "Mobile FOB 1", "AAM-29 Scythe: 1 / 4", "Dustbowl Highway Strip 5,7km",
            "Missile [ARH] 1,0km", "AFV8 Mobile Air Defense +3,3"
        };
        foreach (string c in cases)
            Console.WriteLine((TryPatternMatch(c) ?? "  (без изменений)") + "   <<<   " + c);
    }
}
