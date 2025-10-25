---
title: "Spring Data FalkorDB"
nav_order: 4
description: "How to use FalkorDB with Spring Data for JPA-style object-graph mapping."
parent: "Integration"
---

# Spring Data FalkorDB

This page describes how to integrate FalkorDB with [Spring Data](https://spring.io/projects/spring-data) using [spring-data-falkordb](https://github.com/FalkorDB/spring-data-falkordb).

## Overview

Spring Data FalkorDB provides JPA-style object-graph mapping for [FalkorDB](https://falkordb.com), enabling developers to use familiar Spring Data patterns and annotations to work with graph databases. This library makes it easy to build high-performance graph-based applications using Spring's data access framework.

## Key Features

- **JPA-style Annotations**: Use familiar `@Node`, `@Relationship`, `@Id`, `@Property` annotations
- **Repository Abstractions**: Implement `FalkorDBRepository<T, ID>` for automatic CRUD operations
- **Query Method Generation**: Support for `findByName`, `findByAgeGreaterThan`, etc.
- **Object-Graph Mapping**: Automatic conversion between Java objects and FalkorDB graph structures
- **Transaction Support**: Built on Spring's robust transaction management
- **High Performance**: Leverages FalkorDB's speed with the official JFalkorDB Java client

## Getting Started

### Installation

Add the following dependencies to your project:

#### Maven

```xml
<dependency>
    <groupId>org.springframework.data</groupId>
    <artifactId>spring-data-falkordb</artifactId>
    <version>1.0.0-SNAPSHOT</version>
</dependency>

<dependency>
    <groupId>com.falkordb</groupId>
    <artifactId>jfalkordb</artifactId>
    <version>0.5.1</version>
</dependency>
```

#### Gradle

```gradle
dependencies {
    implementation 'org.springframework.data:spring-data-falkordb:1.0.0-SNAPSHOT'
    implementation 'com.falkordb:jfalkordb:0.5.1'
}
```

### Entity Mapping

Define your graph entities using Spring Data annotations:

```java
@Node(labels = {"Person", "Individual"})
public class Person {
    
    @Id
    @GeneratedValue
    private Long id;
    
    @Property("full_name")  // Maps to "full_name" property in FalkorDB
    private String name;
    
    private String email;
    private int age;
    
    @Relationship(type = "KNOWS", direction = Relationship.Direction.OUTGOING)
    private List<Person> friends;
    
    @Relationship(type = "WORKS_FOR", direction = Relationship.Direction.OUTGOING)
    private Company company;
    
    // Constructors, getters, and setters...
}

@Node("Company")
public class Company {
    
    @Id
    @GeneratedValue
    private Long id;
    
    private String name;
    private String industry;
    
    @Property("employee_count")
    private int employeeCount;
    
    @Relationship(type = "EMPLOYS", direction = Relationship.Direction.INCOMING)
    private List<Person> employees;
    
    // Constructors, getters, and setters...
}
```

### Repository Interface

Create repository interfaces extending `FalkorDBRepository`:

```java
public interface PersonRepository extends FalkorDBRepository<Person, Long> {
    
    Optional<Person> findByName(String name);
    
    List<Person> findByAgeGreaterThan(int age);
    
    List<Person> findByEmail(String email);
    
    Page<Person> findByAgeGreaterThan(int age, Pageable pageable);
    
    long countByAge(int age);
    
    boolean existsByEmail(String email);
}
```

### Configuration

Configure the FalkorDB connection in your Spring application:

```java
@Configuration
@EnableFalkorDBRepositories
public class FalkorDBConfig {
    
    @Bean
    public FalkorDBClient falkorDBClient() {
        Driver driver = FalkorDB.driver("localhost", 6379);
        return new DefaultFalkorDBClient(driver, "social");
    }
    
    @Bean
    public FalkorDBTemplate falkorDBTemplate(FalkorDBClient client,
                                           FalkorDBMappingContext mappingContext,
                                           FalkorDBEntityConverter converter) {
        return new FalkorDBTemplate(client, mappingContext, converter);
    }
}
```

### Service Usage

Use repositories and templates in your service classes:

```java
@Service
@Transactional
public class PersonService {
    
    @Autowired
    private PersonRepository personRepository;
    
    @Autowired
    private FalkorDBTemplate falkorDBTemplate;
    
    public Person createPerson(String name, String email) {
        Person person = new Person(name, email);
        return personRepository.save(person);
    }
    
    public List<Person> findYoungAdults() {
        return personRepository.findByAgeBetween(18, 30);
    }
    
    public List<Person> findConnectedPeople(int minAge) {
        String cypher = """
            MATCH (p:Person)-[:KNOWS]-(friend:Person) 
            WHERE p.age > $minAge 
            RETURN p, friend
        """;
        Map<String, Object> params = Collections.singletonMap("minAge", minAge);
        return falkorDBTemplate.query(cypher, params, Person.class);
    }
}
```

## Supported Annotations

### @Node

Marks a class as a graph node entity:

```java
@Node("Person")                          // Single label
@Node(labels = {"Person", "Individual"}) // Multiple labels  
@Node(primaryLabel = "Person")           // Explicit primary label
```

### @Id

Marks the entity identifier:

```java
@Id
private String customId;  // Assigned ID

@Id 
@GeneratedValue
private Long id;  // FalkorDB internal ID

@Id
@GeneratedValue(UUIDStringGenerator.class)  
private String uuid;  // Custom generator
```

### @Property

Maps fields to graph properties:

```java
@Property("full_name")
private String name;  // Maps to "full_name" property

private String email;  // Maps to "email" property (default)
```

### @Relationship

Maps relationships between entities:

```java
@Relationship(type = "KNOWS", direction = Relationship.Direction.OUTGOING)
private List<Person> friends;

@Relationship(type = "WORKS_FOR", direction = Relationship.Direction.OUTGOING)
private Company company;

@Relationship(type = "EMPLOYS", direction = Relationship.Direction.INCOMING)  
private List<Person> employees;
```

## Repository Query Methods

Spring Data FalkorDB supports JPA-style query methods with these patterns:

### Query Keywords

- **`findBy...`**: Find entities matching criteria
- **`countBy...`**: Count entities matching criteria  
- **`existsBy...`**: Check if entities exist matching criteria
- **`deleteBy...`**: Delete entities matching criteria

### Supported Operations

```java
// Exact match
findByName(String name)

// Comparison operations  
findByAgeGreaterThan(int age)
findByAgeGreaterThanEqual(int age)
findByAgeLessThan(int age)

// Range queries
findByAgeBetween(int start, int end)

// String operations
findByNameContaining(String substring)
findByNameStartingWith(String prefix)
findByNameIgnoreCase(String name)

// Sorting and pagination
findAllByOrderByNameAsc()
findByAgeGreaterThan(int age, Pageable pageable)

// Logical operations
findByNameAndAge(String name, int age)
findByNameOrEmail(String name, String email)
```

## Twitter Integration Example

The library includes a comprehensive Twitter-like integration test that demonstrates real-world usage patterns. This example creates a social graph with users, tweets, follows, and hashtags.

### Entity Examples

#### TwitterUser Entity

```java
@Node(labels = { "User", "TwitterUser" })
public class TwitterUser {
    @Id @GeneratedValue
    private Long id;
    
    @Property("username") private String username;
    @Property("display_name") private String displayName;
    @Property("email") private String email;
    @Property("bio") private String bio;
    @Property("follower_count") private Integer followerCount;
    @Property("verified") private Boolean verified;
    @Property("created_at") private LocalDateTime createdAt;
    
    @Relationship(value = "FOLLOWS", direction = OUTGOING)
    private List<TwitterUser> following;
    
    @Relationship(value = "POSTED", direction = OUTGOING)
    private List<Tweet> tweets;
}
```

#### Tweet Entity

```java
@Node(labels = { "Tweet" })
public class Tweet {
    @Id @GeneratedValue
    private Long id;
    
    @Property("text") private String text;
    @Property("created_at") private LocalDateTime createdAt;
    @Property("like_count") private Integer likeCount;
    @Property("retweet_count") private Integer retweetCount;
    
    @Relationship(value = "POSTED", direction = INCOMING)
    private TwitterUser author;
    
    @Relationship(value = "HAS_HASHTAG", direction = OUTGOING)
    private List<Hashtag> hashtags;
}
```

## Advanced Configuration

### Connection Pool Settings

```java
@Bean
public FalkorDBClient falkorDBClient() {
    Driver driver = FalkorDB.driver("localhost", 6379);
    // Configure connection pool if needed
    return new DefaultFalkorDBClient(driver, "myapp");
}
```

### Custom Converters

```java
@Configuration
public class FalkorDBConfig {
    
    @Bean
    public FalkorDBCustomConversions customConversions() {
        return new FalkorDBCustomConversions(Arrays.asList(
            new LocalDateTimeToStringConverter(),
            new StringToLocalDateTimeConverter()
        ));
    }
}
```

### Transaction Configuration

```java
@Configuration
@EnableTransactionManagement
public class FalkorDBTransactionConfig {
    
    @Bean
    public FalkorDBTransactionManager transactionManager(FalkorDBClient client) {
        return new FalkorDBTransactionManager(client);
    }
}
```

## Reference

- [GitHub Repository](https://github.com/FalkorDB/spring-data-falkordb)
- [Spring Data Documentation](https://spring.io/projects/spring-data)
- [JFalkorDB Java Client](https://github.com/falkordb/jfalkordb)
