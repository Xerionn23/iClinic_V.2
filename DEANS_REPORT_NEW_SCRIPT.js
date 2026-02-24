// Complete Alpine.js module for President/Deans Dashboard with Database Connectivity
function reportsModule() {
    return {
        // Basic initialization
        init() {
            console.log('🚀 Initializing President/Deans Dashboard...');
            
            // Initialize feather icons
            if (typeof feather !== 'undefined') {
                setTimeout(() => feather.replace(), 250);
                setTimeout(() => feather.replace(), 500);
                setTimeout(() => feather.replace(), 1000);
            }
            
            // Load dashboard data from database
            this.loadDashboardData();
            this.loadRecentReports();
            
            // Auto-refresh every 30 seconds
            setInterval(() => {
                this.loadDashboardData();
                this.loadRecentReports();
            }, 30000);
            
            // Handle mobile sidebar behavior
            this.handleMobileResize();
            window.addEventListener('resize', () => this.handleMobileResize());
        },
        
        // Handle mobile responsive behavior
        handleMobileResize() {
            if (window.innerWidth < 768) {
                this.sidebarCollapsed = true;
            }
        },
        
        // Basic state
        sidebarCollapsed: window.innerWidth < 768,
        sidebarHovered: false,
        userDropdown: false,
        loading: true,
        error: null,
        
        // KPI Data (will be loaded from database)
        kpiData: {
            totalStudents: 0,
            clinicVisits: 0,
            healthAlerts: 0,
            criticalCases: 0
        },
        
        // Student Health Data
        studentStats: {
            totalReports: 0,
            thisWeek: 0
        },
        
        studentFilters: {
            department: 'all',
            severity: 'all'
        },
        
        recentStudentReports: [],
        
        // Chart references
        severityChart: null,
        monthlyVisitsChart: null,
        departmentChart: null,
        
        // Load Dashboard Statistics from Database
        async loadDashboardData() {
            try {
                console.log('📊 Loading dashboard statistics...');
                const response = await fetch('/api/deans-president/dashboard-stats');
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                if (data.success) {
                    console.log('✅ Dashboard data loaded:', data);
                    
                    // Update KPI cards
                    this.kpiData = data.kpi;
                    
                    // Initialize or update charts
                    setTimeout(() => {
                        this.initHealthSeverityChart(data.severityData);
                        this.initMonthlyVisitsChart(data.monthlyVisits);
                        this.initDepartmentChart(data.departmentReports);
                    }, 500);
                    
                    this.loading = false;
                } else {
                    throw new Error(data.error || 'Failed to load dashboard data');
                }
            } catch (error) {
                console.error('❌ Error loading dashboard data:', error);
                this.error = error.message;
                this.loading = false;
            }
        },
        
        // Load Recent Student Reports from Database
        async loadRecentReports() {
            try {
                console.log('📋 Loading recent reports...');
                const response = await fetch('/api/deans-president/recent-reports');
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                if (data.success) {
                    console.log('✅ Recent reports loaded:', data.reports.length, 'reports');
                    this.recentStudentReports = data.reports;
                    this.studentStats.totalReports = data.reports.length;
                    
                    // Count this week's reports
                    const oneWeekAgo = new Date();
                    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
                    this.studentStats.thisWeek = data.reports.filter(r => {
                        const reportDate = new Date(r.date);
                        return reportDate >= oneWeekAgo;
                    }).length;
                }
            } catch (error) {
                console.error('❌ Error loading recent reports:', error);
            }
        },
        
        // Health Severity Distribution Chart (Doughnut)
        initHealthSeverityChart(severityData) {
            const ctx = document.getElementById('healthSeverityChart');
            if (!ctx) {
                console.warn('⚠️ healthSeverityChart canvas not found');
                return;
            }
            
            // Destroy existing chart if it exists
            if (this.severityChart) {
                this.severityChart.destroy();
            }
            
            // Prepare data
            const criticalCount = severityData.find(d => d.severity === 'critical')?.count || 0;
            const moderateCount = severityData.find(d => d.severity === 'moderate')?.count || 0;
            const minorCount = severityData.find(d => d.severity === 'minor')?.count || 0;
            
            console.log('📊 Severity Chart Data:', { criticalCount, moderateCount, minorCount });
            
            this.severityChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Critical', 'Moderate', 'Minor'],
                    datasets: [{
                        data: [criticalCount, moderateCount, minorCount],
                        backgroundColor: ['#ef4444', '#f59e0b', '#10b981'],
                        borderWidth: 0,
                        cutout: '60%'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.parsed || 0;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                                    return `${label}: ${value} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
        },
        
        // Monthly Visits Trend Chart (Line)
        initMonthlyVisitsChart(monthlyData) {
            const ctx = document.getElementById('monthlyVisitsChart');
            if (!ctx) {
                console.warn('⚠️ monthlyVisitsChart canvas not found');
                return;
            }
            
            // Destroy existing chart if it exists
            if (this.monthlyVisitsChart) {
                this.monthlyVisitsChart.destroy();
            }
            
            // Prepare data
            const labels = monthlyData.map(d => {
                const [year, month] = d.month.split('-');
                const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                return monthNames[parseInt(month) - 1];
            });
            const visits = monthlyData.map(d => d.visits);
            
            console.log('📈 Monthly Visits Chart Data:', { labels, visits });
            
            this.monthlyVisitsChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Clinic Visits',
                        data: visits,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(0,0,0,0.1)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        },
        
        // Department Reports Chart (Bar)
        initDepartmentChart(departmentData) {
            const ctx = document.getElementById('departmentChart');
            if (!ctx) {
                console.warn('⚠️ departmentChart canvas not found');
                return;
            }
            
            // Destroy existing chart if it exists
            if (this.departmentChart) {
                this.departmentChart.destroy();
            }
            
            // Prepare data - take top 5 departments
            const topDepartments = departmentData.slice(0, 5);
            const labels = topDepartments.map(d => {
                // Shorten department names for better display
                const name = d.department;
                if (name.length > 25) {
                    return name.substring(0, 22) + '...';
                }
                return name;
            });
            const counts = topDepartments.map(d => d.count);
            
            console.log('📊 Department Chart Data:', { labels, counts });
            
            this.departmentChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Clinic Visits',
                        data: counts,
                        backgroundColor: '#10b981',
                        borderRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(0,0,0,0.1)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        },
        
        // Manual refresh function
        async refreshData() {
            console.log('🔄 Manual refresh triggered');
            this.loading = true;
            await this.loadDashboardData();
            await this.loadRecentReports();
            
            // Re-initialize feather icons
            if (typeof feather !== 'undefined') {
                setTimeout(() => feather.replace(), 100);
            }
        },
        
        // Export functions
        exportStudentReport() {
            alert('Exporting Student Health Report... (Feature coming soon)');
        },
        
        exportAppointmentReport() {
            alert('Exporting Appointment Report... (Feature coming soon)');
        },
        
        exportInventoryReport() {
            alert('Exporting Inventory Report... (Feature coming soon)');
        },
        
        exportMonthlyReport() {
            alert('Exporting Monthly Clinic Visits Report... (Feature coming soon)');
        }
    }
}
