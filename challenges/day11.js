/*
--- Day 11: Seating System ---
Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#). For example, the initial seat layout might look like this:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable and always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:

If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes occupied:

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
After a second round, the seats with four or more occupied adjacent seats become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?
*/

const fs = require("fs");
const filename = "./challenges/data/day11data.txt";

function countNeighborsByIdx(rowIdx, colIdx, seatingChart) {
    const height = seatingChart.length;
    const width = seatingChart[rowIdx].length;

    // console.log("height:", height, "- width:", width);

    let counts = {
        open: 0,
        taken: 0,
    };

    const rowRange = [-1, 0, 1];
    const colRange = [-1, 0, 1];
    if (rowIdx === 0) {
        rowRange.shift();
    } else if (rowIdx === height - 1) {
        rowRange.pop();
    }
    if (colIdx === 0) {
        colRange.shift();
    } else if (colIdx === width - 1) {
        colRange.pop();
    }

    for (let i = rowRange[0]; i <= rowRange[rowRange.length - 1]; i++) {
        // console.log("===========");
        const ri = i + rowIdx;
        for (let c = colRange[0]; c <= colRange[colRange.length - 1]; c++) {
            if (i === 0 && c === 0) {
                continue;
            }
            const ci = c + colIdx;
            if (seatingChart[ri][ci] === "L") {
                counts.open += 1;
            }
            if (seatingChart[ri][ci] === "#") {
                counts.taken += 1;
            }
            // console.log(ri, ci, seatingChart[ri][ci]);
        }
    }
    // console.log(counts);
    return counts;
}

function replaceAt(idx, char, string) {
    return string.substring(0, idx) + char + string.substring(idx + 1);
}

function simulate(seatingChart) {
    let predictedChart = [...seatingChart];
    let hasChanged = true;

    while (hasChanged) {
        // console.log("before", predictedChart);
        hasChanged = false;
        const nextChart = [];
        for (let ri = 0; ri < predictedChart.length; ri++) {
            let updatedRow = "";
            for (let ci = 0; ci < predictedChart[ri].length; ci++) {
                if (predictedChart[ri][ci] === ".") {
                    updatedRow += ".";
                    continue;
                }
                // console.log("row", ri, "col", ci);
                const count = countNeighborsByIdx(ri, ci, predictedChart);

                if (predictedChart[ri][ci] === "L" && count.taken === 0) {
                    updatedRow += "#";
                    hasChanged = true;
                } else if (predictedChart[ri][ci] === "#" && count.taken >= 4) {
                    updatedRow += "L";
                    hasChanged = true;
                } else {
                    updatedRow += predictedChart[ri][ci];
                }
            }
            nextChart.push(updatedRow);
        }
        // console.log(nextChart);
        predictedChart = [...nextChart];
        // console.log("after", predictedChart);
        // console.log(hasChanged);
    }

    return predictedChart;
}

function countOccupied(seatingChart) {
    let occupied = 0;
    for (row of seatingChart) {
        for (seat of row) {
            if (seat === "#") {
                occupied += 1;
            }
        }
    }

    return occupied;
}

fs.readFile(filename, "utf8", function (err, text) {
    if (err) throw err;
    console.log("OK: " + filename);
    const data = text.toString().split(new RegExp("\\r?\\n"));

    // console.log(data);
    // console.log(data.length);
    const predictedChart = simulate(data);
    const occupiedCount = countOccupied(predictedChart);
    console.log("Part 1: ", occupiedCount);
});
