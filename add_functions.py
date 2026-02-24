import re

# Read the file
with open(r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Reports.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The functions to add
functions_to_add = '''
                scrollToChart() {
                    if (this.selectedChartFilter === 'all') {
                        this.showAllCharts();
                        return;
                    }
                    document.querySelectorAll('[data-chart-container]').forEach(container => {
                        container.style.display = 'none';
                    });
                    const chartElement = document.getElementById(this.selectedChartFilter);
                    if (chartElement) {
                        const container = chartElement.closest('[data-chart-container]');
                        if (container) {
                            container.style.display = 'block';
                            container.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            container.classList.add('ring-4', 'ring-blue-400', 'ring-opacity-50');
                            setTimeout(() => {
                                container.classList.remove('ring-4', 'ring-blue-400', 'ring-opacity-50');
                            }, 2000);
                        }
                    }
                },
                
                showAllCharts() {
                    document.querySelectorAll('[data-chart-container]').forEach(container => {
                        container.style.display = 'block';
                    });
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                },
                
                resetFilters() {
                    this.selectedChartFilter = 'all';
                    this.selectedPeriod = 'month';
                    this.selectedDepartment = 'all';
                    this.showAllCharts();
                    this.updateCharts();
                },
'''

# Find the first occurrence of getDepartmentName and add functions after it
pattern = r"(getDepartmentName\(dept\) \{[^}]+\}\s+return names\[dept\] \|\| 'All Departments';\s+\},)\s+"

replacement = r"\1" + functions_to_add + "\n                "

# Replace only the first occurrence
content_new = re.sub(pattern, replacement, content, count=1)

# Write back
with open(r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Reports.html', 'w', encoding='utf-8') as f:
    f.write(content_new)

print("✅ Functions added successfully!")
