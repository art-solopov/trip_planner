import {Alpine} from "alpinejs";

const KEYFRAMES_TRANSFORM = [
    {},
    {transform: 'translateX(100%)'}
]

const ANIM_LENGTH = 250
const ANIM_HEIGHT_DELAY = 100

export default function() {
    return {
        async remove() {
            const element = this.$root

            const keyframesHeight = [
                {height: `${element.offsetHeight}px`},
                {height: '0px'}
            ]

            let animationTransform = element.animate(KEYFRAMES_TRANSFORM, {duration: ANIM_LENGTH, fill: "forwards"})
            let animationHeight = element.animate(keyframesHeight, {delay: ANIM_HEIGHT_DELAY, duration: ANIM_LENGTH - ANIM_HEIGHT_DELAY, fill: "forwards"});

            await Promise.all([animationHeight.finished, animationTransform.finished])
            this.$root.remove()
        }
    }
}