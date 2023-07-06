class Utils {
    constructor() {
        this.$loadingContainer = $("#loading-container");
    }

    static average = arr => arr.reduce( ( p, c ) => p + c, 0 ) / arr.length;

    _notify(icon, message, type, delay) {
        return $.notify(
            {
                icon: icon,
                message: message
            },
            {
                type: type,
                delay: delay,
                allow_duplicates: true,
                offset: 10,
                timer: 1000,
                spacing: 10,
                z_index: 2000,
                mouse_over: 'pause',
                newest_on_top: false,
                animate: {
                    enter: 'animated fadeInUp faster',
                    exit: 'animated fadeOutDown faster'
                },
                placement: {
                    from: "top",
                    align: "center"
                },
                template: `
                    <div data-notify="container" class="col-xs-12 alert alert-{0} main-notify" role="alert">
                        <div aria-hidden="true" class="close ml-2" data-notify="dismiss">&times;</div>
                        <span data-notify="icon"></span>
                        <span data-notify="title">{1}</span>
                        <span data-notify="message text-nowrap">{2}</span>
                        <div class="progress" data-notify="progressbar">
                            <div class="progress-bar progress-bar-{0}" role="progressbar"
                                aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>
                        </div>
                        <a href="{3}" target="{4}" data-notify="url"></a>
                    </div>
                `
            }
        );
    }

    showError(message, delay = 3000) {
        this._notify("fa fa-bug", message, 'danger', delay);
    }

    showWarn(message, delay = 3000) {
        this._notify("fa fa-warning", message, 'warning', delay);
    }

    showInfo(message, delay = 3000) {
        this._notify("fa fa-info-circle text-primary", message, 'info', delay);
    }

    showSuccess(message, delay = 3000) {
        this._notify("fa fa-check", message, 'success', delay);
    }

    showAlert(message, delay = 3000) {
        this._notify("", message, 'dark', delay);
    }

    startBusy() {
        this.$loadingContainer.fadeIn(500);
    }

    endBusy() {
        this.$loadingContainer.finish().hide()
    }

    sendRequest(url, data, successCallback, errorCallback) {
        let config = {
            type: 'POST',
            url: url,
            async: true,
            success: (resp) => {
                if (resp.status) {
                    successCallback && successCallback(resp.data);
                } else {
                    errorCallback && errorCallback(resp.message);
                    this.showWarn(resp.message);
                    this.endBusy(-1);
                }
            },
            failure: (err) => {
                errorCallback && errorCallback(err);
                this.showWarn(err);
                this.endBusy(-1);
            },
            error: (xhr, textStatus, thrownError) => {
                errorCallback && errorCallback(thrownError || textStatus);
                this.showWarn(thrownError || textStatus);
                this.endBusy(-1);
            }
        }
        if (data) {
            config.data = JSON.stringify(data);
            config.contentType = "application/json; charset=utf-8";
            config.dataType = "json";
        }
        return $.ajax(config);
    }

    sendRequestFile(url, fileData, successCallback, errorCallback) {
        let config = {
            type: 'POST',
            url: url,
            contentType: false,
            processData: false,
            success: (resp) => {
                if (resp.status) {
                    successCallback && successCallback(resp.data);
                } else if (resp && typeof resp != 'object') {
                    successCallback && successCallback(resp);
                } else {
                    errorCallback && errorCallback(resp.message);
                }
            },
            failure: (err) => {
                errorCallback && errorCallback(err);
            },
            error: (xhr, textStatus, thrownError) => {
                errorCallback && errorCallback(thrownError || textStatus);
            }
        }
        if (fileData) {
            config.data = fileData;
        }
        return $.ajax(config);
    }
}

var utils = new Utils();
