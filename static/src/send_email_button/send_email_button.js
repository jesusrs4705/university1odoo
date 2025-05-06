/** @odoo-module */
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";

class SendEmailButton extends Component {
    static template = "university1.SendEmailButton";
    static props = {
        ...standardWidgetProps,
        method: String,
        title: String,
    };

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
    }

    async onClick() {
        const result = await this.orm.call(
            this.props.record.resModel,
            this.props.method,
            [this.props.record.resId]
        );
        
        if (result && result.params) {
            this.notification.add(
                result.params.message,
                { type: result.params.type }
            );
        }
    }
}

export const sendEmailButton = {
    component: SendEmailButton,
    extractProps: ({ attrs }) => {
        return {
            method: attrs.method,
            title: attrs.title || "Send Email",
        };
    },
};

registry.category("view_widgets").add("send_email_button", sendEmailButton);