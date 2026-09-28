async function api(url, options = {}) {

    const response = await fetch(
        url,
        {
            credentials: "same-origin",
            ...options
        }
    );

    let data = {};

    try {
        data = await response.json();
    }

    catch (_) {
        data = {};
    }

    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Something went wrong"
        );
    }

    return data;
}


function showMessage(
    text,
    error = true
) {

    const el =
        document.getElementById(
            "form-message"
        );

    if (el) {

        el.textContent = text;

        el.style.color =
            error
                ? "#c43f3f"
                : "#26734d";
    }
}


async function logout() {

    await api(
        "/logout",
        {
            method: "POST"
        }
    );

    window.location = "/";
}


function bindLoginForm() {

    const form =
        document.getElementById(
            "login-form"
        );

    form.addEventListener(
        "submit",
        async event => {

            event.preventDefault();

            const body =
                Object.fromEntries(
                    new FormData(form)
                );

            try {

                await api(
                    "/login",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(body)
                    }
                );

                window.location =
                    "/dashboard";

            }

            catch (error) {

                showMessage(
                    error.message
                );
            }
        }
    );
}


function bindRegisterForm() {

    const form =
        document.getElementById(
            "register-form"
        );

    form.addEventListener(
        "submit",
        async event => {

            event.preventDefault();

            const body =
                Object.fromEntries(
                    new FormData(form)
                );

            try {

                await api(
                    "/register",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(body)
                    }
                );

                window.location =
                    "/dashboard";

            }

            catch (error) {

                showMessage(
                    error.message
                );
            }
        }
    );
}


function money(number) {

    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0
        }
    ).format(number);
}


function renderResult(result) {

    const element =
        document.getElementById(
            "results"
        );

    element.className =
        "result-card";

    element.innerHTML = `

        <div class="result-header">

            <p class="eyebrow">
                AI PLAN
            </p>

            <h2>
                ${escapeHtml(result.title)}
            </h2>

            <p class="summary">
                ${escapeHtml(result.summary)}
            </p>

            <strong>
                Estimated total:
                ${money(result.estimated_total)}
            </strong>

            <span class="muted">
                · Remaining:
                ${money(result.remaining_budget)}
            </span>

        </div>


        <h3>
            Budget allocation
        </h3>


        <div class="allocation">

            ${result.allocations
                .map(
                    allocation => `

                    <div class="allocation-row">

                        <span>
                            ${escapeHtml(
                                allocation.category
                            )}
                        </span>

                        <b>
                            ${money(
                                allocation.amount
                            )}
                            ·
                            ${allocation.percentage}%
                        </b>

                    </div>
                `
                )
                .join("")}

        </div>


        <h3>
            Recommendations
        </h3>


        ${result.recommendations
            .map(
                recommendation => `

                <article class="recommendation">

                    <h4>
                        ${escapeHtml(
                            recommendation.name
                        )}
                    </h4>

                    <div class="muted">

                        ${escapeHtml(
                            recommendation.category
                        )}

                        ·

                        ${escapeHtml(
                            recommendation.platform
                        )}

                    </div>

                    <div class="price">

                        ${money(
                            recommendation.estimated_price
                        )}

                    </div>

                    <p class="summary">

                        ${escapeHtml(
                            recommendation.why_it_fits
                        )}

                    </p>

                    <a
                        href="${escapeAttr(
                            recommendation.search_url
                        )}"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Search provider →
                    </a>

                </article>

            `
            )
            .join("")}


        <div class="tips">

            <strong>
                Planning tips
            </strong>

            <ul>

                ${result.tips
                    .map(
                        tip =>
                            `<li>${escapeHtml(
                                tip
                            )}</li>`
                    )
                    .join("")}

            </ul>

        </div>


        <p class="muted">

            ${escapeHtml(
                result.disclaimer
            )}

        </p>

    `;
}


function bindPlannerForm(
    formId,
    endpoint
) {

    const form =
        document.getElementById(
            formId
        );

    form.addEventListener(
        "submit",
        async event => {

            event.preventDefault();

            showMessage(
                "Generating recommendations...",
                false
            );

            const isMultipart =
                form.enctype ===
                "multipart/form-data";

            const options = {
                method: "POST"
            };


            if (isMultipart) {

                options.body =
                    new FormData(form);

            }

            else {

                options.headers = {
                    "Content-Type":
                        "application/json"
                };

                const formData =
                    Object.fromEntries(
                        new FormData(form)
                    );


                if (formData.budget) {

                    formData.budget =
                        Number(
                            formData.budget
                        );
                }


                if (formData.guests) {

                    formData.guests =
                        Number(
                            formData.guests
                        );
                }


                options.body =
                    JSON.stringify(
                        formData
                    );
            }


            try {

                const data =
                    await api(
                        endpoint,
                        options
                    );

                renderResult(
                    data.result
                );

                showMessage(
                    "Recommendation plan generated.",
                    false
                );

            }

            catch (error) {

                if (
                    error.message ===
                    "Login required"
                ) {

                    window.location =
                        "/login";

                }

                else {

                    showMessage(
                        error.message
                    );
                }
            }
        }
    );
}


async function loadHistory(
    targetId = "history-list"
) {

    const target =
        document.getElementById(
            targetId
        );

    try {

        const rows =
            await api("/history");


        if (!rows.length) {

            target.innerHTML = `
                <div class="loading">
                    No recommendations yet.
                </div>
            `;

            return;
        }


        target.innerHTML =
            rows
                .map(
                    row => `

                    <div class="history-item">

                        <div>

                            <h3>
                                ${escapeHtml(
                                    row.result.title
                                )}
                            </h3>

                            <p>

                                ${escapeHtml(
                                    row.planner_type
                                )}

                                ·

                                ${new Date(
                                    row.created_at
                                ).toLocaleString()}

                            </p>

                        </div>


                        <div>

                            <b>
                                ${money(
                                    row.result.total_budget
                                )}
                            </b>

                            <a
                                class="button secondary"
                                href="/recommendations-details/${row.id}"
                                onclick="return openHistory(event, ${row.id})"
                            >
                                View
                            </a>

                        </div>

                    </div>
                `
                )
                .join("");

    }

    catch (error) {

        target.innerHTML = `

            <div class="loading">

                ${escapeHtml(
                    error.message
                )}

                .

                <a href="/login">
                    Log in
                </a>

            </div>

        `;
    }
}


function loadHistoryPage() {

    loadHistory(
        "history-list"
    );
}


function loadDashboardHistory() {

    loadHistory(
        "dashboard-history"
    );
}


async function openHistory(
    event,
    id
) {

    event.preventDefault();

    try {

        const result =
            await api(
                `/recommendations-details/${id}`
            );


        const target =
            document.getElementById(
                "history-list"
            ) ||
            document.getElementById(
                "dashboard-history"
            );


        target.innerHTML = `

            <div class="result-card">

                ${resultHtml(
                    result.result
                )}

                <p>

                    <a href="/history-page">
                        ← Back to history
                    </a>

                </p>

            </div>
        `;

    }

    catch (error) {

        alert(
            error.message
        );
    }


    return false;
}


function resultHtml(result) {

    return `

        <div class="result-header">

            <p class="eyebrow">

                ${escapeHtml(
                    result.title
                )}

            </p>

            <p>

                ${escapeHtml(
                    result.summary
                )}

            </p>

            <strong>

                ${money(
                    result.estimated_total
                )}

                estimated

            </strong>

        </div>


        ${result.recommendations
            .map(
                recommendation => `

                <article class="recommendation">

                    <h4>

                        ${escapeHtml(
                            recommendation.name
                        )}

                    </h4>

                    <p>

                        ${escapeHtml(
                            recommendation.why_it_fits
                        )}

                    </p>

                    <a
                        href="${escapeAttr(
                            recommendation.search_url
                        )}"
                        target="_blank"
                        rel="noopener"
                    >

                        Search
                        ${escapeHtml(
                            recommendation.platform
                        )}
                        →

                    </a>

                </article>
            `
            )
            .join("")}

    `;
}


function escapeHtml(value) {

    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,
        character => ({

            "&": "&amp;",

            "<": "&lt;",

            ">": "&gt;",

            '"': "&quot;",

            "'": "&#039;"

        }[character])
    );
}


function escapeAttr(value) {

    return escapeHtml(
        value
    );
}