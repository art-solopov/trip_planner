import { Application } from 'stimulus'

export function createApp(controllers = []) {
    const app = Application.start()

    for (let controller of controllers) {
        let [name, klass] = controller
        app.register(name, klass)
    }

    return app
}

export function initComponent(component) {
    let app = {}
    if (component.controllers) {
        app.stimulusApp = createApp(component.controllers)
    }

    return app
}
