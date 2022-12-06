class Clock {
    #digits = []
    time = new Date(0, 0, 0, 0, 0, 0, 0)
    increment = (by) => {
        this.time.setSeconds(this.time.getSeconds() + by)
        const n = this.#digits.length

        let seconds = this.time.getSeconds()
        this.#digits[n - 1].dataset.value = `${seconds % 10}`
        this.#digits[n - 2].dataset.value = `${parseInt(seconds / 10) % 10}`

        let minutes = this.time.getMinutes()
        this.#digits[n - 3].dataset.value = `${minutes % 10}`
        this.#digits[n - 4].dataset.value = `${parseInt(minutes / 10) % 10}`

        let hours = this.time.getHours()
        this.#digits[n - 5].dataset.value = `${hours % 10}`
        this.#digits[n - 6].dataset.value = `${parseInt(hours / 10) % 10}`
    }

    constructor(clockHolder) {
        // Hours
        this.#digits.push(document.createElement('div'))
        this.#digits.push(document.createElement('div'))
        // Minutes
        this.#digits.push(document.createElement('div'))
        this.#digits.push(document.createElement('div'))
        // Seconds
        this.#digits.push(document.createElement('div'))
        this.#digits.push(document.createElement('div'))

        this.#digits.forEach((it) => {
            it.classList.add('s7d-digit')
            it.dataset.value = '0'
            clockHolder.append(it)
        })
    }
}