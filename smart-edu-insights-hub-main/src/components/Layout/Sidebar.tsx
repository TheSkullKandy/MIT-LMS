
import { useState, useEffect } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { BookOpen, Calendar, FileText, GraduationCap, LineChart, Users, Video } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarTrigger,
  useSidebar,
} from "@/components/ui/sidebar";

interface UserData {
  email: string;
  userType: string;
  name: string;
  isLoggedIn: boolean;
}

const AppSidebar = () => {
  // Use state property instead of collapsed which doesn't exist in the context
  const { state } = useSidebar();
  const collapsed = state === "collapsed";
  const location = useLocation();
  const [userData, setUserData] = useState<UserData | null>(null);
  
  useEffect(() => {
    const userDataString = localStorage.getItem("lms-user");
    if (userDataString) {
      const parsedUserData = JSON.parse(userDataString);
      setUserData(parsedUserData);
    }
  }, []);
  
  // Define navigation items based on user type
  const studentItems = [
    { title: "Dashboard", path: "/dashboard", icon: LineChart },
    { title: "Courses", path: "/courses", icon: BookOpen },
    { title: "Assignments", path: "/assignments", icon: FileText },
    { title: "Virtual Classes", path: "/classes", icon: Video },
    { title: "Calendar", path: "/calendar", icon: Calendar },
  ];
  
  const facultyItems = [
    { title: "Dashboard", path: "/dashboard", icon: LineChart },
    { title: "My Courses", path: "/courses", icon: BookOpen },
    { title: "Assignments", path: "/assignments", icon: FileText },
    { title: "Virtual Classes", path: "/classes", icon: Video },
    { title: "Students", path: "/students", icon: GraduationCap },
    { title: "Calendar", path: "/calendar", icon: Calendar },
  ];
  
  const navItems = userData?.userType === "faculty" ? facultyItems : studentItems;
  const isActive = (path: string) => location.pathname === path;
  const isExpanded = navItems.some((item) => isActive(item.path));
  const getNavStyles = ({ isActive }: { isActive: boolean }) => 
    cn(
      "flex items-center rounded-md px-3 py-2 text-sm transition-colors",
      isActive ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium" : "hover:bg-sidebar-accent/50"
    );

  return (
    <Sidebar
      className={cn(
        "border-r border-border transition-all duration-300",
        collapsed ? "w-14" : "w-64"
      )}
      collapsible="icon"
    >
      <SidebarTrigger className="m-2 self-end" />
      
      <SidebarContent>
        <div className={cn(
          "mb-4 flex items-center justify-center py-2",
          collapsed ? "px-2" : "px-4"
        )}>
          {collapsed ? (
            <div className="flex h-9 w-9 items-center justify-center rounded bg-primary">
              <span className="text-lg font-bold text-white">M</span>
            </div>
          ) : (
            <div className="flex items-center space-x-2">
              <div className="flex h-9 w-9 items-center justify-center rounded bg-primary">
                <span className="text-lg font-bold text-white">M</span>
              </div>
              <span className="text-lg font-bold text-sidebar-foreground">MIT LMS</span>
            </div>
          )}
        </div>
        
        <div className={cn(
          "mb-6 flex flex-col items-center justify-center",
          collapsed ? "px-2" : "px-4"
        )}>
          {userData && (
            <>
              <div className="mb-2 flex h-12 w-12 items-center justify-center rounded-full bg-white text-primary">
                <span className="text-xl font-bold">{userData.name[0].toUpperCase()}</span>
              </div>
              {!collapsed && (
                <div className="text-center">
                  <p className="font-medium text-sidebar-foreground">{userData.name}</p>
                  <p className="text-xs text-sidebar-foreground/80 capitalize">
                    {userData.userType}
                  </p>
                </div>
              )}
            </>
          )}
        </div>
        
        <SidebarGroup>
          <SidebarGroupLabel className={collapsed ? "sr-only" : ""}>
            Navigation
          </SidebarGroupLabel>
          
          <SidebarGroupContent>
            <SidebarMenu>
              {navItems.map((item) => (
                <SidebarMenuItem key={item.path}>
                  <SidebarMenuButton asChild>
                    <NavLink to={item.path} className={getNavStyles}>
                      <item.icon className="mr-2 h-5 w-5" />
                      {!collapsed && <span>{item.title}</span>}
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
};

export default AppSidebar;
