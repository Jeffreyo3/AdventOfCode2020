/* 
--- Day 16: Ticket Translation ---
As you're walking to yet another connecting flight, you realize that one of the legs of your re-routed trip coming up is on a high-speed train. However, the train ticket you were given is in a language you don't understand. You should probably figure out what it says before you get to the train station after the next flight.

Unfortunately, you can't actually read the words on the ticket. You can, however, read the numbers, and so you figure out the fields these tickets must have and the valid ranges for values in those fields.

You collect the rules for ticket fields, the numbers on your ticket, and the numbers on other nearby tickets for the same train service (via the airport security cameras) together into a single document you can reference (your puzzle input).

The rules for ticket fields specify a list of fields that exist somewhere on the ticket and the valid ranges of values for each field. For example, a rule like class: 1-3 or 5-7 means that one of the fields in every ticket is named class and can be any value in the ranges 1-3 or 5-7 (inclusive, such that 3 and 5 are both valid in this field, but 4 is not).

Each ticket is represented by a single line of comma-separated values. The values are the numbers on the ticket in the order they appear; every ticket has the same format. For example, consider this ticket:

.--------------------------------------------------------.
| ????: 101    ?????: 102   ??????????: 103     ???: 104 |
|                                                        |
| ??: 301  ??: 302             ???????: 303      ??????? |
| ??: 401  ??: 402           ???? ????: 403    ????????? |
'--------------------------------------------------------'
Here, ? represents text in a language you don't understand. This ticket might be represented as 101,102,103,104,301,302,303,401,402,403; of course, the actual train tickets you're looking at are much more complicated. In any case, you've extracted just the numbers in such a way that the first number is always the same specific field, the second number is always a different specific field, and so on - you just don't know what each position actually means!

Start by determining which tickets are completely invalid; these are tickets that contain values which aren't valid for any field. Ignore your ticket for now.

For example, suppose you have the following notes:

class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets by considering only whether tickets contain values that are not valid for any field. In this example, the values on the first nearby ticket are all valid for at least one field. This is not true of the other three nearby tickets: the values 4, 55, and 12 are are not valid for any field. Adding together all of the invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.

Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?
*/

const fs = require("fs");
const filename = "./challenges/data/day16data.txt";

function processData(arr) {
    if (arr.length < 1) {
        return null;
    }

    const data = {
        keyConstraints: {},
        ticket: [],
        nearbyTickets: [],
    };

    let findingKeys = true;
    let idx = 0;

    // save all keys to object/dict
    while (findingKeys === true && idx < arr.length) {
        // console.log(arr[idx]);
        if (!arr[idx]) {
            findingKeys = false;
            idx += 2;
            break;
        }
        const split = arr[idx].split(": ");
        data.keyConstraints[split[0]] = split[1]
            .split(" or ")
            .map((item) => item.split("-"));

        idx += 1;
    }

    // save my ticket
    data.ticket = arr[idx].split(",");
    idx += 3;

    // save all other tickets
    while (idx < arr.length) {
        if (!arr[idx]) {
            idx += 1;
            continue;
        }

        data.nearbyTickets.push(arr[idx].split(","));
        idx += 1;
    }

    return data;
}

function validateTicket(keyConstraints, numArr) {
    const numbers = {};
    // const isValid = [];
    // console.log(Object.keys(keys), Object.keys(keys).length);
    // for (let i = 0; i < Object.keys(keys).length; i++) isValid.push(false);

    // let keyI = 0;
    for (const key in keyConstraints) {
        for (let i = 0; i < numArr.length; i++) {
            if (numbers[numArr[i]] === undefined) {
                numbers[numArr[i]] = false;
            }
            if (
                (+numArr[i] >= +keyConstraints[key][0][0] &&
                    +numArr[i] <= +keyConstraints[key][0][1]) ||
                (+numArr[i] >= +keyConstraints[key][1][0] &&
                    +numArr[i] <= keyConstraints[key][1][1])
            ) {
                // isValid[keyI] = true;
                numbers[numArr[i]] = true;
            }
        }
        // keyI += 1;
    }
    // console.log(numbers);
    // for (bool of isValid) if (!bool) return false;

    // return invalid value
    for (const num in numbers) if (!numbers[num]) return +num;

    return true;
}

function scanningErrorRate(keyConstraints, ticketArr) {
    errorRate = 0;

    for (const ticket of ticketArr) {
        const res = validateTicket(keyConstraints, ticket);
        if (res !== true) {
            errorRate += res;
        }
    }

    return errorRate;
}

/* 
--- Part Two ---
Now that you've identified which tickets contain invalid values, discard those tickets entirely. Use the remaining valid tickets to determine which field is which.

Using the valid ranges for each field, determine what order the fields appear on the tickets. The order is consistent between all tickets: if seat is the third field, it is the third field on every ticket, including your ticket.

For example, suppose you have the following notes:

class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
Based on the nearby tickets in the above example, the first position must be row, the second position must be class, and the third position must be seat; you can conclude that in your ticket, class is 12, row is 11, and seat is 13.

Once you work out which field is which, look for the six fields on your ticket that start with the word departure. What do you get if you multiply those six values together?
*/

function discardInvalidTickets(keyConstraints, ticketArr) {
    const newArr = [];
    for (const ticket of ticketArr) {
        if (validateTicket(keyConstraints, ticket) === true) {
            newArr.push(ticket);
        }
    }
    return newArr;
}

function findTicketPattern(keyConstraints, validTicketArr) {
    // save patern as key: ticket idx
    const pattern = {};

    for (const key in keyConstraints) {
        allTrue = false;
        idx = 0;
        while (idx < validTicketArr[0].length) {
            allTrue = true;
            for (let i = 0; i < validTicketArr.length; i++) {
                // console.log(validTicketArr[i][idx]);
                const range1 =
                    +validTicketArr[i][idx] >= +keyConstraints[key][0][0] &&
                    +validTicketArr[i][idx] <= +keyConstraints[key][0][1];
                const range2 =
                    +validTicketArr[i][idx] >= +keyConstraints[key][1][0] &&
                    +validTicketArr[i][idx] <= +keyConstraints[key][1][1];
                const valid = range1 || range2;
                if (!valid) {
                    allTrue = false;
                }
            }
            if (allTrue) {
                // save every idx where all tickets match
                if (!pattern[key]) {
                    pattern[key] = new Set();
                }
                pattern[key].add(idx);
            }
            idx += 1;
        }
    }

    const keys = {};
    let remaining = validTicketArr[0].length;
    while (remaining > 0) {
        // find key with single item, save it to keys & delete value
        // from pattern obj
        let singleValue = null;
        for (const key in pattern) {
            if (pattern[key].size === 1) {
                singleValue = pattern[key].values().next().value;
                keys[key] = singleValue;
                delete pattern[key];
                break;
            }
        }

        // go through remaining keys and remove from sets
        for (const key in pattern) {
            if (pattern[key].has(singleValue)) {
                pattern[key].delete(singleValue);
            }
        }
        remaining -= 1;
    }

    return keys;
}

function returnTicketDetails(keys, ticket) {
    const ticketDetails = {};
    for (key in keys) {
        ticketDetails[key] = ticket[keys[key]];
    }
    return ticketDetails;
}

function part2Product(obj) {
    let product = 1;
    for (key in obj) {
        if (key.includes("departure")) {
            product *= obj[key];
        }
    }
    return product;
}

fs.readFile(filename, "utf8", function (err, text) {
    if (err) throw err;
    console.log("OK: " + filename);
    const input = text.toString().split(new RegExp("\\r?\\n"));

    const data = processData(input);

    const errorRate = scanningErrorRate(
        data.keyConstraints,
        data.nearbyTickets
    );
    console.log("Part 1:", errorRate);

    data.validNearbyTickets = discardInvalidTickets(
        data.keyConstraints,
        data.nearbyTickets
    );

    data.keys = findTicketPattern(data.keyConstraints, data.validNearbyTickets);

    const myTicket = returnTicketDetails(data.keys, data.ticket);
    const productOfDeparture = part2Product(myTicket);
    console.log("Part 2:", productOfDeparture);
});
