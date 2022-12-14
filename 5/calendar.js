class Calendar {
    months = [
        "Styczeń", "Luty", "Marzec", "Kwiecień",
        "Maj", "Czerwiec", "Lipiec", "Sierpień",
        "Wrzesień", "Październik", "Listopad", "Grudzień"
    ]

    static info = [
        {
            date: '5-12',
            message: '<b>Zamieszczenie zadań etapu powiatowego</b><br> BIOLOGIA, FIZYKA, INFORMATYKA',
            important: true
        },
        {
            date: '9-12',
            message: '<b>Przesłanie rozwiązanych zadań</b><br>CHEMIA, MATEMATYKA, KOMPETENCJE SPOŁECZNE',
            important: true
        },
        {
            date: '16-12',
            message: '<b>Przesłanie rozwiązanych zadań</b><br> BIOLOGIA, FIZYKA, INFORMATYKA',
            important: true
        },
        {
            date: '10-1',
            message: '<b>Ogłoszenie wstępnych wyników etapu powiatowego</b>',
            important: true
        },
        {
            date: '18-1',
            message: '<b>Ogłoszenie końcowych wyników etapu powiatowego oraz osób zakwalifikowanych</b>',
            important: true
        },
    ]

    constructor(parent) {
        this.parent = parent
        this.currentMonth = 0
        const nullableCalendarData = localStorage.getItem("calendarData")
        if (nullableCalendarData == null) {
            this.calendarData = []
        } else {
            const calendarData = JSON.parse(nullableCalendarData)
            this.calendarData = calendarData
            console.log(calendarData)
        }

        this.generate()
    }

    selectMonth = (next) => {
        console.log(this.parent.childNodes)
        this.parent
            .querySelector(`.month_holder:nth-child(${this.currentMonth + 1}`)
            .classList.remove('active')
        const prev = this.currentMonth
        this.currentMonth = Math.min(Math.max(this.currentMonth + next, 0), 11)
        if (prev === this.currentMonth && next)
            new Audio("Windows Ding.wav").play()
        this.parent
            .querySelector(`.month_holder:nth-child(${this.currentMonth + 1}`)
            .classList.add('active')

        this.parent.parentNode
            .querySelector('.current_month_display')
            .innerText = this.months[(this.currentMonth + new Date().getMonth()) % 12]
    }

    generate = () => {
        while (this.parent.firstChild) {
            this.parent.removeChild(this.parent.firstChild)
        }

        const currentMonth = new Date().getMonth() + 1
        let allDays = []
        for (let i = 0; i < 12; i++) {
            const monthHolder = createMonthHolder(currentMonth + i)
            const days = createMonthDays(monthHolder)
            allDays.push(...days)
            monthHolder.calendar = this
            this.parent.append(monthHolder)
        }
        this.fillDays(allDays)
        this.selectMonth(0)
    }

    fillDays = (days) => {
        for (let event of [...this.calendarData, ...Calendar.info]) {
            const {date, message, important=false} = event
            const el = days.filter((it) => {
                return it.dataset.date === date
            })[0]

            const eventView = this.createEventView(event)
            el.querySelector('.event_holder').append(eventView)
        }
    }

    addEvent = (dayElement, info) => {
        const newEvent = {
            date: dayElement.dataset.date,
            message: info
        }
        this.calendarData.push(newEvent)
        this.save()

        this.generate()
    }

    createEventView = (event) => {
        const element = document.createElement('div')
            const info = document.createElement('p')
            info.innerHTML = event.message
            element.append(info)
            if (event.important) element.classList.add('important')
            if (!event.important) {
                const remove = document.createElement('button')
                remove.innerText = "Usuń"
                remove.onclick = () => {
                    this.calendarData = this.calendarData.filter((it) => {
                        return !(it.message === event.message && it.date === event.date)
                    })

                    this.generate()
                }
                element.append(remove)
            }
        return element
    }

    save = () => {
        localStorage.setItem("calendarData", JSON.stringify(this.calendarData))
    }
}

function createMonthHolder(monthNumber) {
    const holder = document.createElement('div')
    holder.classList.add('month_holder')
    holder.dataset.monthNumber = `${(monthNumber - 1) % 12 + 1}`
    return holder
}

function createMonthDays(holder) {
    const year = new Date().getFullYear() % 4 === 0
    const monthNumber = parseInt(holder.dataset.monthNumber)
    const days = [31, 28 + year, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][monthNumber - 1]
    for (let i = 1; i <= days; i++) {
        const day = document.createElement('div')
        day.classList.add('month_day')
        day.dataset.date = `${i}-${monthNumber}`

        const today = new Date()
        const dayNumberDate = new Date(today.getFullYear(), monthNumber - 1, i)
        day.dataset.dayname = [
            "Niedziela",
            "Poniedziałek",
            "Wtorek",
            "Środa",
            "Czwartek",
            "Piątek",
            "Sobota",
        ][dayNumberDate.getDay()]
        if (day.dataset.date === `${today.getDate()}-${today.getMonth() + 1}`) {
            day.classList.add('today')
        }
        const eventHolder = document.createElement('div')
            eventHolder.classList.add('event_holder')
        day.append(eventHolder)

        const addNewButton = document.createElement('button')
            addNewButton.textContent = 'dodaj'
            addNewButton.style.padding = '5px 10px'
            addNewButton.onclick = () => {
                holder.calendar.addEvent(day, prompt("Podaj informacje: "))
            }
        day.append(addNewButton)

        holder.append(day)
    }
    return holder.children
}
