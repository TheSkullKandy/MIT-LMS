
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userType, setUserType] = useState("student");
  const [isLoading, setIsLoading] = useState(false);
  
  const { toast } = useToast();
  const navigate = useNavigate();
  
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    // In a real application, this would be an API call
    setTimeout(() => {
      setIsLoading(false);
      // Demo login - in a real app this would validate credentials
      localStorage.setItem("lms-user", JSON.stringify({ 
        email,
        userType,
        name: userType === "faculty" ? 
          email.split("@")[0].split('.').map(name => name.charAt(0).toUpperCase() + name.slice(1)).join(' ') : 
          email.split("@")[0],
        isLoggedIn: true
      }));
      
      toast({
        title: "Login successful",
        description: `Welcome back, ${userType === "faculty" ? "Professor " : ""}${email.split("@")[0]}!`,
      });
      
      navigate("/dashboard");
    }, 1500);
  };
  
  return (
    <Card className="w-[400px] shadow-lg">
      <CardHeader>
        <CardTitle className="text-2xl text-center">MIT LMS</CardTitle>
        <CardDescription className="text-center">
          Sign in to access your learning portal
        </CardDescription>
      </CardHeader>
      
      <CardContent>
        <Tabs defaultValue="student" onValueChange={setUserType} className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-6">
            <TabsTrigger value="student">Student</TabsTrigger>
            <TabsTrigger value="faculty">Faculty</TabsTrigger>
          </TabsList>
          
          <TabsContent value="student">
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="student-email">Student Email</Label>
                <Input 
                  id="student-email"
                  type="email" 
                  placeholder="student@university.edu" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="student-password">Password</Label>
                  <a href="#" className="text-xs text-blue-600 hover:underline">
                    Forgot password?
                  </a>
                </div>
                <Input 
                  id="student-password"
                  type="password" 
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <Button type="submit" className="w-full bg-lms-student" disabled={isLoading}>
                {isLoading ? "Signing in..." : "Sign in as Student"}
              </Button>
            </form>
          </TabsContent>
          
          <TabsContent value="faculty">
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="faculty-email">Faculty Email</Label>
                <Input 
                  id="faculty-email"
                  type="email" 
                  placeholder="professor@university.edu" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="faculty-password">Password</Label>
                  <a href="#" className="text-xs text-blue-600 hover:underline">
                    Forgot password?
                  </a>
                </div>
                <Input 
                  id="faculty-password"
                  type="password" 
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <Button type="submit" className="w-full bg-primary" disabled={isLoading}>
                {isLoading ? "Signing in..." : "Sign in as Faculty"}
              </Button>
              
              <div className="mt-2 text-xs text-gray-500">
                <p>As faculty, you'll have access to:</p>
                <ul className="list-disc pl-5 mt-1">
                  <li>Course management tools</li>
                  <li>Student performance tracking</li>
                  <li>Assignment grading</li>
                  <li>Virtual classroom controls</li>
                </ul>
              </div>
            </form>
          </TabsContent>
        </Tabs>
      </CardContent>
      
      <CardFooter className="flex justify-center">
        <p className="text-sm text-gray-500">
          Need help? Contact <a href="#" className="text-blue-600 hover:underline">IT Support</a>
        </p>
      </CardFooter>
    </Card>
  );
};

export default LoginForm;
