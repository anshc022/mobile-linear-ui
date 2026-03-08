# Freelance Project Tracker - UX Design Specs

**Target Audience:** Freelancers managing multiple tasks/projects.
**Design Philosophy:** "High Density & Efficiency." Minimize whitespace, maximize data visibility. Clean, professional, utility-first aesthetic (linear, structured).

## 1. Layout Structure
**Split View:**
- **Left Sidebar (Filters & Navigation):** Fixed width (e.g., 250px). Darker background or distinct border.
- **Main Content (Task List):** Fluid width. White/Light Gray background.

---

## 2. Feature Specifications

### A. Smart Date Grouping (Main Content)
**Logic:**
- Tasks are sorted by `due_date` or `created_at` (descending).
- Inject sticky headers for date boundaries.

**Visuals:**
- **Headers:** Small, uppercase, bold, muted color (e.g., `text-xs font-bold text-gray-500 uppercase tracking-wider`).
- **Groups:**
    - "Today"
    - "Yesterday"
    - "This Week" (if older than yesterday but within 7 days)
    - Specific Date (e.g., "March 5th, 2024") for older items.

**Mockup Concept:**
```text
TODAY
[ ] Fix Login Bug           [Bug]      In Progress   2h ago
[ ] Update Homepage Hero    [Feature]  Pending       4h ago

YESTERDAY
[x] Client Meeting Notes    [Admin]    Done          1d ago
```

### B. Category & Status Filters (Sidebar)
**Component: Filter Panel**
- **Status (Multi-select Checkboxes):**
    - [ ] Pending
    - [ ] In Progress
    - [ ] Done (Completed)
- **Category (Pills/Tags):**
    - Click to toggle: `[Bug]`, `[Feature]`, `[Design]`, `[Admin]`
- **Date Range (Mini Calendar or Dropdown):**
    - Options: "All Time", "Last 7 Days", "Last 30 Days", "Custom Range".

### C. Professional 'Freelancer' Aesthetic (Visual Style)
**Typography:**
- Headings: Sans-serif (Inter/Roboto), clean.
- Data/IDs: Monospaced (JetBrains Mono/Fira Code) for prices, hours, or task IDs.
- Size: Base text `13px` or `14px` (dense).

**Spacing:**
- Row Padding: `py-2` or `py-3` (compact).
- Gap: `gap-2` between elements.
- Borders: Subtle separators (`border-b border-gray-100`) instead of cards with heavy shadows.

**Colors:**
- Background: `bg-white` for rows.
- Hover: `hover:bg-gray-50` for interactivity.
- Badges:
    - **Bug:** Red/Pink text + bg.
    - **Feature:** Blue/Indigo text + bg.
    - **Done:** Green text + bg or strikethrough text.
    - **Pending:** Gray/Yellow.

### D. History View
**Implementation:**
- **Option 1 (Tab):** A top-level tab "Active" vs "History".
- **Option 2 (Filter-based):** "History" is simply the state where specific filters (Status: Done) are active.
    - **Recommendation:** Use a dedicated **"Archive/History"** tab in the Sidebar navigation to keep the main view focused on active work.

**Search in History:**
- Search bar at the top of the History view.
- Filters remain available but default to "All Time" and "Status: Done".

---

## 3. Implementation Notes for Bolt (Frontend)

### Component Hierarchy
1.  `AppShell` (Layout grid: Sidebar + Main)
2.  `FilterSidebar`
    *   `StatusFilter`
    *   `CategoryFilter`
    *   `DateRangePicker`
3.  `TaskListView`
    *   `TaskListHeader` (Sort controls, global search)
    *   `TaskGroup` (The date header + list of tasks)
        *   `TaskRow` (Individual task item)

### State Management (React/Store)
- `filterState`: `{ status: [], categories: [], dateRange: { start, end } }`
- `groupedTasks`: Derived state. Function: `groupTasksByDate(tasks, filterState)`

### CSS Classes (Tailwind suggestions)
- **Task Row:** `flex items-center justify-between p-3 border-b border-gray-100 hover:bg-gray-50 transition-colors text-sm`
- **Date Header:** `sticky top-0 bg-white/95 backdrop-blur py-2 px-3 text-xs font-bold text-gray-400 uppercase border-b border-gray-100 z-10`
- **Sidebar:** `w-64 border-r border-gray-200 h-screen p-4 flex flex-col gap-6 bg-gray-50`
