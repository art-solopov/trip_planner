import { Application } from 'stimulus'

export default function createApp(controllers = []) {
    const app = Application.start()

    for (let controller of controllers) {
        let [name, klass] = controller
        app.register(name, klass)
    }

    return app
}
