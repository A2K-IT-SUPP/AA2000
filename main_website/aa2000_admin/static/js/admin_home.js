$(document).ready(function() {

    function getDashboardData() {

    $.ajax({
        url: `/admin/home/get/data/dashboard`,
        type: 'GET',
        success: function(response) {
            console.log(response);
            placeDashboardData(response)
        },
        error: function(xhr, status, error) {
            console.log(error)
        }
    })

    }
    


    getDashboardData()


    function placeDashboardData(response) {
        var data = response.data        
        
        var productTotal = data.total_products_count
        var productChange = data.count_change_product
        var productPercentage = data.count_change_product_percentage

        var brandTotal = data.total_brands_count
        var brandChange = data.count_change_brand
        var brandPercentage = data.count_change_brand_percentage

        var inquiryTotal = data.total_inquiries_count
        var inquiryChange = data.count_change_inquiry
        var inquiryPercentage = data.count_change_inquiry_percentage
        var inquiryStatusCount = data.total_inquiry_status_count

        var articleTotal = data.total_articles_count
        var articleChange = data.count_change_article
        var articlePercentage = data.count_change_article_percentage
        var top_five_articles = data.top_five_articles

        var jobsTotal = data.total_jobs_count
        var jobsChange = data.count_change_job
        var jobsPercentage = data.count_change_job_percentage

        var visitorsCountPerDay = data.visitors_count
        var productsVisits = data.products_visits
        var brandsVisits = data.brands_visits

        // product data
        $('#product_percent').text(`${productPercentage} %`)
        $('#total_products').text(`${productTotal}`)
        $('#change_products').text(`${productChange}`)


        // brand data
        $('#brand_percent').text(`${brandPercentage} %`)
        $('#total_brands').text(`${brandTotal}`)
        $('#change_brands').text(`${brandChange}`)

        // jobs data
        $('#job_percent').text(`${jobsPercentage} %`)
        $('#total_jobs').text(`${jobsTotal}`)
        $('#change_jobs').text(`${jobsChange}`)

        // inquiry data
        $('#inquiry_percent').text(`${inquiryPercentage} %`)
        $('#total_inquiry').text(`${inquiryTotal}`)
        $('#change_inquiry').text(`${inquiryChange}`)

        // article data
        $('#article_percent').text(`${articlePercentage} %`)
        $('#total_article').text(`${articleTotal}`)
        $('#change_article').text(`${articleChange}`)

        for (let index = 0; index < top_five_articles.length; index++) {
            const list_item = `<li class="list-group-item">${top_five_articles[index].article_title}</li>`
            $('#top_five_articles').append(list_item)
        }
        
        // Predefined statuses
        const allStatuses = ["DONE", "NEW", "PENDING"];

        // Create a function to get the count for each status
        const getStatusCount = (status) => {
        const statusData = inquiryStatusCount.find(item => item.status === status);
        return statusData ? statusData.count : 0; // Return count or 0 if status not found
        };

        // Prepare the data
        const labels = allStatuses;
        const dataValues = allStatuses.map(status => getStatusCount(status));

        const backgroundColors = [
            '#22c197',
            '#eee8a9',
            '#ff72b2'
        ];

        const inquiry_config = {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Inquiry Status',
                    data: dataValues,
                    backgroundColor: backgroundColors,
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
        
        const inquiryStatusContainer = $('#total_count_status_inquiry')
        const inquiryStatusChart = new Chart(inquiryStatusContainer, inquiry_config)



        // for general visitors chart
        const dateLabels = visitorsCountPerDay.map(item => item.date);
        const dateCounts = visitorsCountPerDay.map(item => item.visit_count);

        const labelBgColors = Array(dateCounts.length).fill('#4c7df9');
        const labelBorderColors = Array(dateCounts.length).fill('#0a2fbf');

        const visitor_count_config = {
            type: 'bar',
            data: {
                labels: dateLabels,
                datasets: [{
                    label: 'General Visitors',
                    data: dateCounts,
                    backgroundColor: labelBgColors,
                    borderColor: labelBorderColors,
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
                                    return value;
                                }
                            },
                            stepSize: 1,
                        },
                        beginAtZero: true,
                    }
                }
            }
        }


        const generalVisitorsContainer = $('#general_visitors_chart');
        const generalVisitorsChart = new Chart(generalVisitorsContainer, visitor_count_config)


        // for product visits week
        const productLabels = productsVisits.map(item => item.product_name)
        const productValues = productsVisits.map(item => item.count)

        const productLabelBgColors = Array(productValues.length).fill('#6a91fa');
        const productLabelBorderColors = Array(productValues.length).fill('#1833c9');

        const product_views_config = {
            type: 'bar',
            data: {
                labels: productLabels,
                datasets: [{
                    label: 'Product Visits this Week',
                    data: productValues,
                    backgroundColor: productLabelBgColors,
                    borderColor: productLabelBorderColors,
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
    
        const productsViewsContainer = $('#products_views_chart')
        const productsViewsChart = new Chart(productsViewsContainer, product_views_config)


        // for brands views
        const brandLabels = brandsVisits.map(item => item.brand_name);
        const brandValues = brandsVisits.map(item => item.count);

        const brandLabelBgColors = Array(brandValues.length).fill('#5b84ff');
        const brandLabelBorderColors = Array(brandValues.length).fill('#1431a8')

        const brand_view_config = {
            type: 'bar',
            data: {
                labels: brandLabels,
                datasets: [{
                    label: 'Brand Visits this Week',
                    data: brandValues,
                    backgroundColor: brandLabelBgColors,
                    borderColor: brandLabelBorderColors,
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

        const brandViewsContainer = $('#brands_views_chart')
        const brandViewsChart = new Chart(brandViewsContainer, brand_view_config)


    }
})
