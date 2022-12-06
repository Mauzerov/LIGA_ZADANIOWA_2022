document.querySelectorAll('.clock').forEach((it) => {
    let clock = new Clock(it)
    setInterval(() => {
        clock.increment(1)
    }, 1000)
})

document.querySelectorAll('.s7d-digit').forEach((el) => {
    for (let i = 0; i < 7; i++) {
        const segment = document.createElement('div')
        el.append(segment)
    }
})