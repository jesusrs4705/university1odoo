/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { FormController } from "@web/views/form/form_controller";

export class StudentFormController extends FormController {
    setup() {
        super.setup();
        this.actionService = useService("action");
        this.notificationService = useService("notification");
        this.orm = useService("orm");
    }

    async sendTestEmail() {
        const record = this.model.root;
        const email = record.data.email;
        
        if (!email) {
            this.notificationService.add(
                "Please set an email address first.",
                { type: "warning" }
            );
            return;
        }

        try {
            await this.orm.call(
                "university.student",
                "sendTestEmail",
                [record.resId]
            );

            this.notificationService.add(
                `A sample email has been sent to ${email}`,
                { type: "success" }
            );
        } catch (error) {
            this.notificationService.add(
                error.message || "Error sending email",
                { type: "danger" }
            );
        }
    }
}

registry.category("views").add("student_form", {
    ...registry.category("views").get("form"),
    Controller: StudentFormController,
});