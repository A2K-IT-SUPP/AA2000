$(document).ready(function() {

    // functions to get data
    function getProductsData() {
        $.ajax({
            url: `/admin/reports/get/data/products`,
            type: "GET",
            success: function(response) {
                console.log(response);
                placeProductsData(response)
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
            }
        })
    }

    function getBrandsData() {
        $.ajax({
            url: `/admin/reports/get/data/brands`,
            type: "GET",
            success: function(response) {
                console.log(response);
                placeBrandsData(response)
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
            }
        })
    }

    
    function getInquiriesData() {
        $.ajax({
            url: `/admin/reports/get/data/inquiries`,
            type: "GET",
            success: function(response) {
                console.log(response);
                placeInquiriesData(response)
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
            }
        })
    }


    function getArticlesData() {
        $.ajax({
            url: `/admin/reports/get/data/articles`,
            type: "GET",
            success: function(response) {
                console.log(response);
                placeArticlesData(response)
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
            }
        })
    }



    // initiate the functions
    getProductsData()
    getBrandsData()
    getInquiriesData()
    getArticlesData()







    // functions to display data
    // display products data
    function placeProductsData(response) {

        var page_obj = response.data

        var totalProductsCount = page_obj.total_products_count
        var perSystemCount = page_obj.per_system_count
        var perSystemCategoryCount = page_obj.per_system_category_count
        var topViewedProducts_day = page_obj.top_viewed_products_day
        var topViewedProducts_week = page_obj.top_viewed_products_week
        var topViewedProducts_month = page_obj.top_viewed_products_month
        var topViewedProducts_year = page_obj.top_viewed_products_year
        var productRecentlyAdded = page_obj.product_recently_added



       $('#total_products').text(`${totalProductsCount}`) 

        const productSystemLabels = perSystemCount.map(item => item.system_name)
        const productSystemValues = perSystemCount.map(item => item.count)

        const productSystemLabelBgColors = Array(productSystemValues.length).fill('#6a91fa');
        const productSystemLabelBorderColors = Array(productSystemValues.length).fill('#1833c9');

        const product_system_config = {
            type: 'bar',
            data: {
                labels: productSystemLabels,
                datasets: [{
                    label: 'Product Count per System',
                    data: productSystemValues,
                    backgroundColor: productSystemLabelBgColors,
                    borderColor: productSystemLabelBorderColors,
                    borderWidth: 1,
                }]
            },
            options: {
                responsive: true,
                aspectRatio: 1.9,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        ticks: {
                            callback: function (value) {
                                if (Number.isInteger(value)) {
                                    return value
                                }
                            },
                            stepSize: 1,
                        },
                        beginAtZero: true,
                    }
                }
            }
        }

        const productsSystemContainer = $('#product_system_container')
        const productsSystemChart = new Chart(productsSystemContainer, product_system_config)


        Object.values(perSystemCategoryCount).forEach((system, index) => {
            const tabId = `tab-${index}`;
            const tabItem = document.createElement('li')
            tabItem.classList.add('nav-item')
            tabItem.innerHTML = `
                <button
                class="nav-link ${index === 0 ? 'active' : ''}"
                id="${tabId}-tab"
                data-bs-toggle="tab"
                data-bs-target="#${tabId}"
                type="button"
                role="tab"
                aria-controls="${tabId}"
                aria-selected="${index === 0 ? 'true' : 'false'}"
                >
                ${system.system_name}
                </button>
            `;

            $('#product_system_tab_panel_area').append(tabItem);


            const contentItem = document.createElement('div');
            contentItem.className = `tab-pane fade ${index==0 ? 'show active' : ''}`;
            contentItem.id = tabId;
            contentItem.role = 'tabpanel';
            contentItem.setAttribute('aria-labelledby', `${tabId}-tab`);
            contentItem.innerHTML =`
                <h3>${system.system_name}</h3>
                <canvas id="chart-${index}" width="400" height="400"></canvas>
            `;

            $('#tab_content_area').append(contentItem);
        });


        Object.values(perSystemCategoryCount).map((system,index) => {
            const ctx = $(`#chart-${index}`);
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: system.categories.map(category => category.category_name),
                    datasets: [{
                        label: `${system.system_name} Product Count`,
                        data: system.categories.map(category => category.count),
                        backgroundColor: '#6a91fa',
                        borderColor: '#1833c9',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    aspectRatio: 1.9,
                    maintainAspectRatio: true,
                    scales: {
                        y: {
                            ticks: {
                                callback: function (value) {
                                    if (Number.isInteger(value)) {
                                        return value;
                                    }
                                },
                                stepSize: 1,
                            },
                            beginAtZero: true
                        }
                    }
                }
            })
        })


        var productViews = [
            topViewedProducts_day,
            topViewedProducts_week,
            topViewedProducts_month,
            topViewedProducts_year,
        ];
        var productViewsTag = ['today', 'week', 'month', 'year'];
        
        productViews.forEach((productView, index) => {
            if (!productView || productView.length === 0) {
                console.warn(`No data available for ${productViewsTag[index]}`);
                return;
            }
        
            const ctx = document.getElementById(`product_views_${productViewsTag[index]}_container`).getContext('2d');
        
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: productView.map(product => product.product_name),
                    datasets: [{
                        label: `Product Count`,
                        data: productView.map(product => product.count),
                        backgroundColor: '#6a91fa',
                        borderColor: '#1833c9',
                        borderWidth: 1,
                    }],
                },
                options: {
                    responsive: true,
                    aspectRatio: 1.9,
                    maintainAspectRatio: true,
                    scales: {
                        y: {
                            ticks: {
                                callback: function (value) {
                                    if (Number.isInteger(value)) {
                                        return value;
                                    }
                                },
                                stepSize: 1,
                            },
                            beginAtZero: true,
                        },
                    },
                },
            });
        });

        productRecentlyAdded.forEach((product, index) => {
            const productName = product.product_name;
            const productSystem = product.system_name;
            const created_at = product.created_at;

            var list_item = `
                <li class="list-group-item">
                    ${productSystem} - ${productName} <span class="text-muted fst-light fst-italic" >${created_at}</span>
                </li>
            `

            $('#recently_added_product').append(list_item)
        })

    }



    // place brands data
    function placeBrandsData(response) {
        var page_obj = response.data

        var totalBrandsCount = page_obj.total_brands_count
        var perSystemCount = page_obj.per_system_count
        var topViewedBrands_day = page_obj.top_viewed_brands_day
        var topViewedBrands_week = page_obj.top_viewed_brands_week
        var topViewedBrands_month = page_obj.top_viewed_brands_month
        var topViewedBrands_year = page_obj.top_viewed_brands_year
        var brandRecentlyAdded = page_obj.brand_recently_added


        $('#total_brands').text(`${totalBrandsCount}`)

        const brandSystemLabels = perSystemCount.map(item => item.system_name)
        const brandSystemValues = perSystemCount.map(item => item.count)

        const brandSystemLabelBgColors = Array(brandSystemValues.length).fill('#6a91fa');
        const brandSystemLabelBorderColors = Array(brandSystemValues.length).fill('#1833c9');

        const brand_system_config = {
            type: 'bar',
            data: {
                labels: brandSystemLabels,
                datasets: [{
                    label: 'Brand Count per System',
                    data: brandSystemValues,
                    backgroundColor: brandSystemLabelBgColors,
                    borderColor: brandSystemLabelBorderColors,
                    borderWidth: 1,
                }]
            },
            options: {
                responsive: true,
                aspectRatio: 1.9,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        ticks: {
                            callback: function (value) {
                                if (Number.isInteger(value)) {
                                    return value
                                }
                            },
                            stepSize: 1,
                        },
                        beginAtZero: true,
                    }
                }
            }
        }

        const brandsSystemContainer = $('#brands_system_container')
        const brandsSystemChart = new Chart(brandsSystemContainer, brand_system_config)



        
        var brandViews = [
            topViewedBrands_day,
            topViewedBrands_week,
            topViewedBrands_month,
            topViewedBrands_year,
        ];
        var brandViewsTag = ['today', 'week', 'month', 'year'];
        
        brandViews.forEach((brandView, index) => {
            if (!brandView || brandView.length === 0) {
                console.warn(`No data available for ${brandViewsTag[index]}`);
                return;
            }
        
            const ctx = document.getElementById(`brand_views_${brandViewsTag[index]}_container`).getContext('2d');
        
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: brandView.map(brand => brand.brand_name),
                    datasets: [{
                        label: `Brand Count`,
                        data: brandView.map(brand => brand.count),
                        backgroundColor: '#6a91fa',
                        borderColor: '#1833c9',
                        borderWidth: 1,
                    }],
                },
                options: {
                    responsive: true,
                    aspectRatio: 1.9,
                    maintainAspectRatio: true,
                    scales: {
                        y: {
                            ticks: {
                                callback: function (value) {
                                    if (Number.isInteger(value)) {
                                        return value;
                                    }
                                },
                                stepSize: 1,
                            },
                            beginAtZero: true,
                        },
                    },
                },
            });
        });

        brandRecentlyAdded.forEach((brand, index) => {
            const brandName = brand.brand_name;
            const brandSystem = brand.system_name;
            const created_at = brand.created_at;

            var list_item = `
                <li class="list-group-item">
                    ${brandSystem} - ${brandName} <span class="text-muted fst-light fst-italic" >${created_at}</span>
                </li>
            `

            $('#recently_added_brand').append(list_item)
        })

    }



    function placeInquiriesData(response) {

        var page_obj = response.data

        var totalInquiriesCount = page_obj.total_inquiries_count
        var perStatusCount = page_obj.per_inquiry_status_count
        var perConcernCount = page_obj.per_inquiry_status_concern
        var receivedInquiries_day = page_obj.inquiries_per_day
        var receivedInquiries_week = page_obj.inquiries_per_week
        var receivedInquiries_month = page_obj.inquiries_per_month
        var receivedInquiries_year = page_obj.inquiries_per_year


        $('#total_inquiries').text(`${totalInquiriesCount}`)


        var inquiriesCountData = [receivedInquiries_day,
                                    receivedInquiries_week,
                                    receivedInquiries_month,
                                    receivedInquiries_year
        ]

        var inquiryCountLabel = ["day", "week", "month", "year"]

        inquiriesCountData.forEach((inquiry, index) => {
            const inquiryTabId = `tab-inquiry-${inquiryCountLabel[index]}`;
            const inquiryTabItem = document.createElement('li')
            inquiryTabItem.classList.add('nav-item')
            inquiryTabItem.innerHTML = `
                <button
                class="nav-link ${index === 0 ? 'active' : ''}"
                id="${inquiryTabId}-tab"
                data-bs-toggle="tab"
                data-bs-target="#${inquiryTabId}"
                type="button"
                role="tab"
                aria-controls="${inquiryTabId}"
                aria-selected="${index === 0 ? 'true' : 'false'}"
                >
                ${inquiryCountLabel[index].toUpperCase()}
                </button>
            `;


            $('#inquiry_count_tab_panel_area').append(inquiryTabItem)


            const inquiryContentItem = document.createElement('div');
            inquiryContentItem.className = `tab-pane fade ${index==0 ? 'show active' : ''}`;
            inquiryContentItem.id = inquiryTabId;
            inquiryContentItem.role = 'tabpanel';
            inquiryContentItem.setAttribute('aria-labelledby', `${inquiryTabId}-tab`);
            inquiryContentItem.innerHTML = `
                <h3>Inquiries Received for this ${inquiryCountLabel[index].toUpperCase()}</h3>
                <canvas id="inquiry-count-chart-${inquiryCountLabel[index]}" width="400" height="400"></canvas>`;

            $('#inquiry_tab_content_area').append(inquiryContentItem)



            const ctx = $(`#inquiry-count-chart-${inquiryCountLabel[index]}`);
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: inquiry.map(item => {
                        const labelKey = inquiryCountLabel[index];
                        return item[labelKey] || 'N/A';
                    }),
                    datasets: [{
                        label: `Inquiry Count this ${inquiryCountLabel[index]}`,
                        data: inquiry.map(item => item.count),
                        backgroundColor: '#6a91fa',
                        borderColor: '#1833c9',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    aspectRatio: 1.9,
                    maintainAspectRatio: true,
                    scales: {
                        y: {
                            ticks:{
                                callback: function(value) {
                                    if (Number.isInteger(value)) {
                                        return value;
                                    }
                                },
                                stepSize: 1,
                            },
                            beginAtZero: true
                        }
                    }
                }
            })
        })

        const inquiryStatusLabel = perStatusCount.map(item => item.status)
        const inquiryStatusValues = perStatusCount.map(item => item.count)

        const inquiryStatusBackgroundColors = [
            '#22c197',
            '#eee8a9',
            '#ff72b2'
        ];

        const inquiry_status_config = {
            type: 'doughnut',
            data: {
                labels: inquiryStatusLabel,
                datasets: [{
                    label: 'Inquiry Status',
                    data: inquiryStatusValues,
                    backgroundColor: inquiryStatusBackgroundColors,
                    hoverOffset: 4
                }],
                },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: 'Inquiry Status Count'
                    }
                },
                responsive: true,
                aspectRatio: 1.3,
                maintainAspectRatio: true,
            }
        }


        const inquiryStatusContainer = $('#inquiries_count_status')
        const inquiryStatusChart = new Chart(inquiryStatusContainer, inquiry_status_config)


        const inquiryConcernLabel = perConcernCount.map(item => item.concern_category_name)
        const inquiryConcernValues = perConcernCount.map(item => item.count)

        const inquiryConcentBackgroundColors = [
            '#22c197', 
            '#eee8a9', 
            '#ff72b2', 
            '#36d6ab', 
            '#f3ecb2', 
            '#ff8abb', 
            '#1da57a'  
        ];

        const inquiry_concern_config = {
            type: 'doughnut',
            data: {
                labels: inquiryConcernLabel,
                datasets: [{
                    label: 'Inquiry Status',
                    data: inquiryConcernValues,
                    backgroundColor: inquiryConcentBackgroundColors,
                    hoverOffset: 4
                }],
                },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: 'Inquiry Status Count'
                    }
                },
                responsive: true,
                aspectRatio: 1.3,
                maintainAspectRatio: true,
            }
        }


        const inquiryConcernContainer = $('#inquiries_count_concerns')
        const inquiryConcernChart = new Chart(inquiryConcernContainer, inquiry_concern_config)
    }



    function placeArticlesData(response) {
        var page_obj = response.data

        var totalArticlesCount = page_obj.total_articles_count
        var perArticleKeyword = page_obj.per_article_keyword
        var topArticles = page_obj.top_ten_articles



        $('#total_articles').text(`${totalArticlesCount}`)

        const articleKeywordsLabel = perArticleKeyword.map(item => item.lower_keywords.toUpperCase())
        const articleKeywordsValues = perArticleKeyword.map(item => item.count)

        const articleKeywordsLabelBgColors = Array(articleKeywordsValues.length).fill('#6a91fa');
        const articleKeywordsLabelBorderColors = Array(articleKeywordsValues.length).fill('#1833c9');


        const article_keyword_count_config = {
            type: 'bar',
            data: {
                labels: articleKeywordsLabel,
                datasets: [{
                    label: 'Number of Articles',
                    data: articleKeywordsValues,
                    backgroundColor: articleKeywordsLabelBgColors,
                    borderColor: articleKeywordsLabelBorderColors,
                    borderWidth: 1,
                }]
            },
            options: {
                responsive: true,
                aspectRatio: 1.9,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        ticks: {
                            callback: function (value) {
                                if (Number.isInteger(value)) {
                                    return value
                                }
                            },
                            stepSize: 1,
                        },
                        beginAtZero: true,
                    }
                }
            }
        }

        const articleKeywordContainer = $('#article_keyword_count_container')
        const articleKeywordChart = new Chart(articleKeywordContainer, article_keyword_count_config)


        topArticles.forEach((article, index) => {
            const articleTitle = article.article_title;
            const articleAuthor = article.article_author;
            const numOfViews = article.count;

            const listItem = document.createElement('li')
            listItem.classList.add('list-group-item', 'd-flex', 'justify-content-between')
            listItem.innerHTML = `
            <h6 class="fw-medium">${articleTitle}</h6>
            <span class="text-muted">${articleAuthor}</span>
            <span class="text-muted">${numOfViews} views</span>
            `

            $('#top_ten_articles').append(listItem)
        })


    }
})