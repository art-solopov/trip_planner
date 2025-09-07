import { Controller } from '@hotwired/stimulus'

const KEYFRAMES_TRANSFORM = [
    {},
    {transform: 'translateX(100%)'}
]

const ANIM_LENGTH = 250
const ANIM_HEIGHT_DELAY=100

export class FlashController extends Controller {
    remove() {
        const keyframesHeight = [
            {height: `${this.element.offsetHeight}px`},
            {height: '0px'}
        ]

        let element = this.element
        let animationTransform = element.animate(KEYFRAMES_TRANSFORM, ANIM_LENGTH)
        let animationHeightFinished = new Promise((resolve) => {
            setTimeout(() => {
                let animationHeight = element.animate(keyframesHeight, ANIM_LENGTH - ANIM_HEIGHT_DELAY)
                animationHeight.finished.then(e => resolve(e))
            }, ANIM_HEIGHT_DELAY);
        })

        Promise.all([animationHeightFinished, animationTransform.finished]).then(() => element.remove())
    }
}
