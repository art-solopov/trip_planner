import {Application} from "@hotwired/stimulus";

function initComponent(app, component) {
    let {stimulusApp} = app
    if (component.controllers) {
        for (let controller of component.controllers) {
            let [name, klass] = controller
            stimulusApp.register(name, klass)
        }
    }
    if (component.init) {
        component.init()
        app.init.push(component.init)
    }

    return app
}

export function createApp(...components) {
    const app = {
        stimulusApp: Application.start(),
        init: []
    }

    for (let component of components) {
        initComponent(app, component)
    }

    return app
}