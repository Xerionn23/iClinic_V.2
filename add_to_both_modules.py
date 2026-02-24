#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read the file
with open(r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Reports.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# The functions to insert
new_functions = """                
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
"""

# Find ALL occurrences of getDepartmentName and add functions after each
insertions_made = 0
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check if this line contains "return names[dept] || 'All Departments';"
    if "return names[dept] || 'All Departments';" in line:
        # Find the closing }, after this
        for j in range(i, min(i+5, len(lines))):
            if lines[j].strip() == '},':
                # Check if functions are already added
                already_has_functions = False
                for k in range(j+1, min(j+10, len(lines))):
                    if 'scrollToChart()' in lines[k]:
                        already_has_functions = True
                        break
                
                if not already_has_functions:
                    lines.insert(j + 1, new_functions)
                    insertions_made += 1
                    print(f"✅ Inserted functions after line {j + 1}")
                    i = j + 1  # Skip past the inserted content
                else:
                    print(f"ℹ️  Functions already exist after line {j + 1}, skipping")
                break
    i += 1

# Write back
with open(r'c:\xampp\htdocs\iClini V.2\pages\staff\Staff-Reports.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\n✅ Total insertions made: {insertions_made}")
print("🔄 Please do a HARD REFRESH: Ctrl + Shift + R")
