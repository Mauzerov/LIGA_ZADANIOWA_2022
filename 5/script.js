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

document.querySelectorAll('.carousel__control').forEach((el) => {
    el.addEventListener('click', (e) => {
        const carousel = e.target.closest('.carousel')
        const items = carousel.querySelectorAll('.carousel__item')
        const activeItem = carousel.querySelector('.carousel__item.active')
        const activeItemIndex = Array.from(items).indexOf(activeItem)
        const direction = parseInt(el.dataset.value)
        const itemToActivate = items[(activeItemIndex + direction + items.length) % items.length]
        carousel.querySelector('.carousel__container').scrollLeft += itemToActivate.offsetWidth * direction
        activeItem.classList.remove('active')
        itemToActivate.classList.add('active')
    })
})