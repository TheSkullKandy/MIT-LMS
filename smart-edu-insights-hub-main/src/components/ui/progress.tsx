
import * as React from "react"

import { cn } from "@/lib/utils"

const Progress = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & {
    value?: number
    max?: number
    fill?: string
  }
>(({ className, value, max = 100, fill, ...props }, ref) => {
  const percentage = value != null ? Math.min(Math.max(value, 0), max) : null

  return (
    <div
      ref={ref}
      role="progressbar"
      aria-valuemin={0}
      aria-valuemax={max}
      aria-valuenow={percentage ?? undefined}
      className={cn(
        "relative h-2 w-full overflow-hidden rounded-full bg-secondary",
        className
      )}
      {...props}
    >
      {percentage != null && (
        <div
          className={cn("h-full w-full flex-1 bg-primary transition-all", fill)}
          style={{ transform: `translateX(-${100 - (percentage / max) * 100}%)` }}
        />
      )}
    </div>
  )
})
Progress.displayName = "Progress"

export { Progress }
