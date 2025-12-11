let inputs_no = 1
const inputs_div = document.querySelector(".inputs");


function add_input() {
    inputs_no += 1

    const input = `
 <div class="input">
        <label for="">Credit </label>
        <input type="number" id="input_${inputs_no}" class="credit" name="">

        <label>Grade </label>
        <select name="" id="grade_${inputs_no}" class="grade">
              <option value="10">O</option>
            <option value="9">A+</option>
            <option value="8">A</option>
            <option value="7">B+</option>
            <option value="6">B</option>
            <option value="5">C</option>
            <option value="4">P</option>
            <option value="0">F</option>
            <option value="0">Ab</option>
        </select>
    </div>
`

    inputs_div.insertAdjacentHTML("beforeend", input)
}

grade_points = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5,
    "P": 4,
    "F": 0,
    "Ab": 0,
    "I": null,
    "*": null,
}


function cal_gpa() {
    let grade_list = []
    let credit_list = []

    for (let i = 1; i <= inputs_no; i++) {
        credit_list.push(Number(document.getElementById(`input_${i}`).value))
        grade_list.push(Number(document.getElementById(`grade_${i}`).value))
    }

    // grade to grade points
    // for (let i = 0; i < grade_list.length; i++) {
    //     let grade = grade_list[i]
    //     grade_list[i] = grade_points[grade]
    // }

    let grade_total = 0
    let credit_total = sum(credit_list)

    for (let i = 0; i < credit_list.length; i++) {
        grade_total += Number(credit_list[i]) * Number(grade_list[i])
        console.log(credit_total,grade_list,credit_list)
    }

    let cgpa = 0
    const result = document.getElementById("result")

    cgpa = (grade_total / credit_total).toFixed(2)
    result.innerText = `Your CPA is :${cgpa}`
}

function sum(arr) {
    let arr_sum = 0
    for (let i = 0; i < arr.length; i++) {
        arr_sum += Number(arr[i])
    }
    return arr_sum
}
