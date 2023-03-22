FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["text_summary/text_summary.csproj", "text_summary/"]
RUN dotnet restore "text_summary/text_summary.csproj"
COPY . .
WORKDIR "/src/text_summary"
RUN dotnet build "text_summary.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "text_summary.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "text_summary.dll"]
